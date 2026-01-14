from typing import Literal, List, Optional, Union

from selectolax.lexbor import LexborHTMLParser as Parser

from ..client import human_get
from ..models import Provider, Country, Phone, Message
from .provider_base import SMSProvider


class ReceiveSMSSProvider(SMSProvider):
    """
    Provider implementation for https://receive-smss.com/.

    This site exposes:
        - A single landing page listing all numbers.
        - Each number includes its country.
        - A message page for each number (no pagination).

    The structure is simple: all countries and numbers are extracted from the
    homepage, and messages are scraped from the number's detail page.
    """

    BASE = Provider.RECEIVESMSS.value

    # ------------------------------------------------------------------
    # Country + number retrieval
    # ------------------------------------------------------------------

    def fetch_countries(self) -> List[Country]:
        """
        Return all countries available on the provider homepage.

        Returns
        -------
        list[Country]
            A list of country dictionaries with:
                - name: str
                - url: None (ReceiveSMSS does not expose per-country URLs)
        """
        return self._fetch_all(key="countries")

    def fetch_numbers(
        self,
        country: Optional[Union[Country, str]] = None,
    ) -> List[Phone]:
        """
        Return all phone numbers, optionally filtered by country.

        Parameters
        ----------
        country : Country | str | None
            - None: return all numbers.
            - str: match by lowercase country name.
            - Country: match by exact dict identity.

        Returns
        -------
        list[Phone]
            Phone entries with:
                - number: str
                - url: str (full message page URL)
                - country: Country
        """
        numbers = self._fetch_all(key="numbers")

        if not country:
            return numbers

        if isinstance(country, str):
            country = country.lower()
            return [nm for nm in numbers if nm["country"]["name"] == country]

        # Country dict provided directly
        return [nm for nm in numbers if nm["country"] == country]

    # ------------------------------------------------------------------
    # Internal scraper for homepage (countries + numbers)
    # ------------------------------------------------------------------

    def _fetch_all(
        self,
        key: Literal["numbers", "countries"] = None,
    ):
        """
        Scrape the provider homepage and extract both countries and numbers.

        Parameters
        ----------
        key : {"numbers", "countries"} | None
            If provided, return only that subset.
            If None, return a dict with both lists.

        Returns
        -------
        list | dict
            Either:
                - list[Country]
                - list[Phone]
                - {"countries": [...], "numbers": [...]}
        """
        res = human_get(self.BASE)
        tree = Parser(res.text)

        out = {"countries": [], "numbers": []}
        seen_countries = set()

        # Each number box contains:
        #   - number
        #   - country name
        #   - link to message page
        for node in tree.css("div#content div.number-boxes-item > a"):
            number_raw = node.css_first("div:nth-child(1)").text(strip=True)
            country_raw = (
                node.css_first("div.number-boxes-item-country")
                .text(strip=True)
                .lower()
            )

            # ReceiveSMSS does not provide country URLs.
            country_obj: Country = {"name": country_raw, "url": None}

            number_obj: Phone = {
                "number": number_raw,
                "url": self.BASE + node.attributes["href"],
                "country": country_obj,
            }

            # Track unique countries
            if country_raw not in seen_countries:
                seen_countries.add(country_raw)
                out["countries"].append(country_obj)

            out["numbers"].append(number_obj)

        return out[key] if key else out

    # ------------------------------------------------------------------
    # Message retrieval
    # ------------------------------------------------------------------

    def fetch_messages(self, phone: Union[Phone, str]) -> List[Message]:
        """
        Retrieve all messages for a given phone number.

        Parameters
        ----------
        phone : Phone | str
            - Phone dict returned by `fetch_numbers`.
            - Or a raw phone string (rarely used).

        Returns
        -------
        list[Message]
            Messages with:
                - sender: str
                - text: str
        """
        # Build the message page URL
        if isinstance(phone, str):
            url = f"{self.BASE}/sms/{phone}/"
        else:
            url = phone["url"]

        res = human_get(url)
        tree = Parser(res.text)

        # Message text and sender appear in parallel lists
        message_nodes = tree.css("div.message_details label+br+span")
        sender_nodes = tree.css("div.message_details > div.senderr > a")

        messages: List[Message] = []

        for msg_node, sender_node in zip(message_nodes, sender_nodes):
            messages.append(
                {
                    "sender": sender_node.text(strip=True),
                    "text": msg_node.text(strip=True),
                }
            )

        return messages

