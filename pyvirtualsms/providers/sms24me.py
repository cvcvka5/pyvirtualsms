import re
from typing import List, Optional, Union

from selectolax.lexbor import LexborHTMLParser as Parser

from ..client import human_get
from ..models import Country, Phone, Message, Provider
from .provider_base import SMSProvider


class SMS24MeProvider(SMSProvider):
    """
    Provider implementation for https://sms24.me/.

    SMS24Me exposes:
        - A country list page.
        - A per‑country page listing numbers.
        - A paginated message page for each number.

    This provider supports pagination, so `fetch_messages` accepts a `page`
    argument and the distributor will pass it when appropriate.
    """

    BASE = Provider.SMS24ME.value

    # ------------------------------------------------------------------
    # Country retrieval
    # ------------------------------------------------------------------

    def fetch_countries(self) -> List[Country]:
        """
        Fetch all available countries from SMS24.me.

        Returns
        -------
        list[Country]
            Each entry contains:
                - name: lowercase country name
                - url: provider-specific country page URL
        """
        url = f"{self.BASE}/en/countries"
        res = human_get(url)
        tree = Parser(res.text)

        return [
            {
                "name": node.text(strip=True).lower(),
                "url": self.BASE + node.attributes["href"],
            }
            for node in tree.css("div.container.mb-3 a.callout")
        ]

    # ------------------------------------------------------------------
    # Number retrieval
    # ------------------------------------------------------------------

    def fetch_numbers(
        self,
        country: Optional[Union[Country, str]] = None,
    ) -> List[Phone]:
        """
        Fetch phone numbers for a given country.

        Parameters
        ----------
        country : Country | str | None
            - None: return numbers from the *first* country only (provider behavior).
            - str: match by lowercase country name.
            - Country: use the provided dict directly.

        Returns
        -------
        list[Phone]
            Phone entries with:
                - number: str
                - url: str (message page base URL)
                - country: Country
        """
        # If a specific country is requested
        if country is not None:
            # Resolve string → Country dict
            if isinstance(country, str):
                target = country.lower()
                for cntry in self.fetch_countries():
                    if cntry["name"] == target:
                        country = cntry
                        break

                # Still a string → no match found
                if isinstance(country, str):
                    raise ValueError(
                        f"No phone number registered to '{country}' exists "
                        f"in provider '{self.BASE}'."
                    )

        # If no country provided, SMS24Me returns numbers for all of the countries
        else:
            numbers: List[Phone] = []
            for country in self.fetch_countries():
                numbers.extend(self.fetch_numbers(country))

            # Provider lists all numbers
            return numbers

        # Fetch numbers for the resolved country
        res = human_get(country["url"])
        tree = Parser(res.text)

        return [
            {
                "number": node.css_first("div.text-primary").text(strip=True),
                "url": self.BASE + node.attributes["href"],
                "country": country,
            }
            for node in tree.css("div.col-sm-12 > a.callout.m-2")
        ]

    # ------------------------------------------------------------------
    # Message retrieval (pagination supported)
    # ------------------------------------------------------------------

    def fetch_messages(
        self,
        phone: Union[Phone, str],
        page: int = 1,
    ) -> List[Message]:
        """
        Fetch messages for a given phone number.

        SMS24Me supports pagination, so the `page` parameter is appended
        to the phone's URL.

        Parameters
        ----------
        phone : Phone | str
            - Phone dict returned by `fetch_numbers`.
            - Or a raw phone string (rare case).
        page : int
            Page number to fetch.

        Returns
        -------
        list[Message]
            Messages with:
                - sender: str
                - text: str
        """
        # Build the message page URL
        if isinstance(phone, str):
            url = f"{self.BASE}/en/numbers/{phone}"
        else:
            url = f"{phone['url']}/{page}"

        res = human_get(url)
        tree = Parser(res.text)

        messages: List[Message] = []

        # Messages appear in <dl><dd> blocks
        for dd in tree.css("dl dd"):
            # Sender text cleanup
            sender = dd.css_first("a").text(strip=True).replace("From: ", "")
            sender = re.sub(r"\s+", " ", sender)

            # Message body cleanup
            text = dd.css_first("span").text(strip=True)
            text = re.sub(r"\s+", " ", text)

            messages.append({"sender": sender, "text": text})

        return messages

