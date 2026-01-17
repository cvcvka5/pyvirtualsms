from typing import List, Optional, Union, no_type_check

from selectolax.lexbor import LexborHTMLParser as Parser

from ..client import human_get
from ..models import Country, Phone, Message, Provider
from .provider_base import SMSProvider


class FreePhoneNumProvider(SMSProvider):
    """
    Provider wrapper for freephonenum.com.
    Handles scraping of countries, numbers, and SMS messages.
    """

    BASE = Provider.FREEPHONENUM.value

    def fetch_countries(self) -> List[Country]:
        """
        Fetch the list of available countries from the provider.

        Returns:
            List[Country]: Each entry contains a name + URL.
        """
        res = human_get(self.BASE)
        tree = Parser(res.text)

        # Country names include a trailing count → strip the last token
        return [
            {
                "name": " ".join(node.text(strip=True).lower().split(" ")[:-1]),
                "url": node.parent.attributes["href"],
            }
            for node in tree.css("div.container div.row a > span:nth-child(1)")
        ]

    def fetch_numbers(self, country: Optional[Union[Country, str]] = None) -> List[Phone]:
        """
        Fetch phone numbers for a given country. If no country is provided,
        recursively fetch numbers for all countries.

        Args:
            country: Country dict or name string.

        Returns:
            List[Phone]: List of phone entries with number + URL.
        """
        # Resolve string → country dict
        if country is not None:
            if isinstance(country, str):
                target = country.lower()
                for cntry in self.fetch_countries():
                    if cntry["name"] == target:
                        country = cntry
                        break

                # Still a string → no match
                if isinstance(country, str):
                    raise ValueError(
                        f"No phone number registered to '{country}' exists "
                        f"in provider '{self.BASE}'."
                    )
        else:
            # No country passed → aggregate all numbers
            numbers: List[Phone] = []
            for cntry in self.fetch_countries():
                numbers.extend(self.fetch_numbers(cntry))
            return numbers

        # Fetch numbers for the resolved country
        res = human_get(country["url"])
        tree = Parser(res.text)

        return [
            {
                "number": node.css_first("div:nth-child(1)").text(strip=True),
                "url": f"{self.BASE}/{node.attributes['href']}",
                "country": country,
            }
            for node in tree.css("div.container a.numbers-btn:not(.disabled)")
        ]

    def fetch_messages(self, phone: Phone) -> List[Message]:
        """
        Fetch SMS messages for a given phone number.

        Args:
            phone: Phone dict containing the message page URL.

        Returns:
            List[Message]: Parsed messages with sender + text.
        """
        res = human_get(phone["url"])
        tree = Parser(res.text)

        out: List[Message] = []

        # Each row contains sender + message text
        for node in tree.css("tbody tr"):
            sender = node.css_first("td:nth-child(2)")
            text = node.css_first("td:nth-child(3)")

            msg = {}
            if text:
                msg["text"] = text.text(strip=True)
                msg["sender"] = sender.text(strip=True) if sender else None

            out.append(msg)

        return out
