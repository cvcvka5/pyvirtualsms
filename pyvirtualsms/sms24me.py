import re
import random
from selectolax.lexbor import LexborHTMLParser as Parser
from typing import List, Optional

from .client import human_get
from .models import Country, Phone, Message, Provider
from .provider_base import SMSProvider


class SMS24MeProvider(SMSProvider):
    """Implementation of the SMS24.me scraping logic."""

    BASE = Provider.SMS24ME.value

    def fetch_countries(self) -> List[Country]:
        url = f"{self.BASE}/en/countries"
        res = human_get(url)
        tree = Parser(res.text)

        return [
            {
                "name": node.text(strip=True).lower(),
                "url": self.BASE + node.attributes["href"]
            }
            for node in tree.css("div.container.mb-3 a.callout")
        ]

    def fetch_numbers(self, country: Optional[Country] = None) -> List[Phone]:
        if not country:
            country = random.choice(self.fetch_countries())

        res = human_get(country["url"])
        tree = Parser(res.text)

        return [
            {
                "number": node.css_first("div.text-primary").text(strip=True),
                "url": self.BASE + node.attributes["href"]
            }
            for node in tree.css("div.col-sm-12 > a.callout.m-2")
        ]

    def fetch_messages(self, phone: Phone, page: int = 1) -> List[Message]:
        res = human_get(f"{phone['url']}/{page}")
        tree = Parser(res.text)

        messages = []
        for dd in tree.css("dl dd"):
            sender = dd.css_first("a").text(strip=True).replace("From: ", "")
            sender = re.sub(r"\s+", " ", sender)

            text = dd.css_first("span").text(strip=True)
            text = re.sub(r"\s+", " ", text)

            messages.append({"sender": sender, "text": text})

        return messages

