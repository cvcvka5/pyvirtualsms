from abc import ABC, abstractmethod
from typing import List, Optional

from ..models import Country, Phone, Message


class SMSProvider(ABC):
    """
    Abstract base class for all SMS provider implementations.

    Each provider must implement the following operations:
        - fetch_countries(): return a list of available countries.
        - fetch_numbers(country): return phone numbers for a given country.
        - fetch_messages(phone): return messages for a specific phone number.

    The goal is to keep the interface minimal and consistent so that
    `GSMDistributor` can interact with any provider interchangeably.
    """

    @abstractmethod
    def fetch_countries(self) -> List[Country]:
        """
        Retrieve all countries supported by the provider.

        Returns
        -------
        list[Country]
            A list of country dictionaries with at least:
                - name: str
                - url: str (provider-specific)
        """
        pass

    @abstractmethod
    def fetch_numbers(self, country: Optional[Country] = None) -> List[Phone]:
        """
        Retrieve phone numbers for a given country.

        Parameters
        ----------
        country : Country | None
            If provided, return numbers only for that country.
            If None, return all numbers (if the provider supports this).

        Returns
        -------
        list[Phone]
            A list of phone dictionaries with:
                - number: str
                - url: str
                - country: Country
        """
        pass

    @abstractmethod
    def fetch_messages(self, phone: Phone) -> List[Message]:
        """
        Retrieve all messages for a given phone number.

        Parameters
        ----------
        phone : Phone
            A phone dictionary returned by `fetch_numbers`.

        Returns
        -------
        list[Message]
            A list of message dictionaries with:
                - sender: str
                - text: str
        """
        pass

