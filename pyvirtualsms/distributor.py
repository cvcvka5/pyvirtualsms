import random
from typing import Optional, List

from .models import Provider, Country, Phone, Message
from .sms24me import SMS24MeProvider


class GSMDistributor:
    """High-level interface for interacting with SMS providers."""

    def __init__(self, provider: Provider):
        self.provider_enum = provider

        match provider:
            case Provider.SMS24ME:
                self.provider = SMS24MeProvider()
            case _:
                raise ValueError(f"Unsupported provider: {provider}")

    def get_countries(self) -> List[Country]:
        return self.provider.fetch_countries()

    def get_numbers(self, country: Optional[Country] = None) -> List[Phone]:
        return self.provider.fetch_numbers(country)

    def get_random_number(self, country: Optional[Country] = None) -> Phone:
        return random.choice(self.get_numbers(country))

    def get_messages(self, phone: Phone, page: int = 1) -> List[Message]:
        return self.provider.fetch_messages(phone, page)

    def __repr__(self) -> str:
        return f"GSMDistributor(provider={self.provider_enum.name})"

