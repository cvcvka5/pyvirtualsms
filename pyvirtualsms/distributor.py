"""
Distributor abstraction over SMS providers.

This module defines `GSMDistributor`, a high-level interface for interacting
with different SMS providers in a consistent way.

Responsibilities:
    - Select the correct provider implementation based on the `Provider` enum.
    - Expose simple methods for fetching countries, numbers, messages.
    - Handle optional pagination support in a provider-agnostic way.
"""

import inspect
import random
from typing import Optional, List, Union

from .models import Provider, Country, Phone, Message
from .providers.sms24me import SMS24MeProvider
from .providers.receivesmss import ReceiveSMSSProvider
from .providers.freephonenum import FreePhoneNumProvider

class GSMDistributor:
    """
    High-level interface for interacting with SMS providers.

    This class wraps a concrete provider implementation and exposes a uniform API:

        - get_countries()
        - get_numbers(country)
        - get_random_number(country)
        - get_messages(phone, page)

    Parameters
    ----------
    provider : Provider
        The provider enum value specifying which backend to use.
    """

    def __init__(self, provider: Provider):
        self.provider_enum = provider

        # Instantiate the concrete provider implementation based on the enum.
        match provider:
            case Provider.SMS24ME:
                self.provider = SMS24MeProvider()
            case Provider.RECEIVESMSS:
                self.provider = ReceiveSMSSProvider()
            case Provider.FREEPHONENUM:
                self.provider = FreePhoneNumProvider()
            case _:
                raise ValueError(f"Unsupported provider: {provider}")

    def get_countries(self) -> List[Country]:
        """
        Fetch all available countries from the current provider.

        Returns
        -------
        list[Country]
            A list of country entries as returned by the provider.
        """
        return self.provider.fetch_countries()

    def get_numbers(
        self,
        country: Optional[Union[Country, str]] = None,
    ) -> List[Phone]:
        """
        Fetch phone numbers for a given country.

        Parameters
        ----------
        country : Country | str | None, optional
            Either:
                - A `Country` dict returned by `get_countries()`, or
                - A country name as a string (case-insensitive, provider-specific),
                - None, meaning "all countries" if the provider supports it.

        Returns
        -------
        list[Phone]
            A list of phone entries for the specified country (or all).
        """
        return self.provider.fetch_numbers(country)

    def get_random_number(
        self,
        country: Optional[Union[Country, str]] = None,
    ) -> Phone:
        """
        Pick a random phone number from the available numbers.

        Parameters
        ----------
        country : Country | str | None, optional
            Country filter(same semantics as `get_numbers`).

        Returns
        -------
        Phone
            A randomly chosen phone entry.

        Raises
        ------
        RuntimeError
            If no numbers are available (empty result from the provider).
        """
        numbers = self.get_numbers(country)
        if not numbers:
            # Empty list usually means network issues, rate limiting, or no data.
            raise RuntimeError(
                "No numbers returned — provider may be empty or rate limited."
            )
        return random.choice(numbers)

    def get_messages(
        self,
        phone: Phone,
        page: Optional[int] = 1,
    ) -> List[Message]:
        """
        Fetch messages for a given phone, with optional pagination.

        This method automatically detects whether the underlying provider
        supports a `page` parameter by inspecting its `fetch_messages` signature.

        For example:
            - Providers without pagination:
                  fetch_messages(phone)
            - Providers with pagination:
                  fetch_messages(phone, page)

        Parameters
        ----------
        phone : Phone
            The phone entry as returned by `get_numbers` or `get_random_number`.
        page : int | None, optional
            Page to request for providers that support pagination. Ignored for
            providers that only implement `fetch_messages(phone)`.

        Returns
        -------
        list[Message]
            A list of messages for the given phone (and page, if applicable).
        """
        # Inspect the provider's `fetch_messages` to determine if it supports pagination.
        sig = inspect.signature(self.provider.fetch_messages)
        params = list(sig.parameters.values())

        # Instance method:
        #   - fetch_messages(phone)        -> 2 parameters in total.
        #   - fetch_messages(phone, page) -> 3 parameters in total.
        if len(params) == 1:
            # Provider does NOT support pagination, ignore `page`.
            return self.provider.fetch_messages(phone)
        else:
            # Provider supports pagination, pass the page argument through.
            return self.provider.fetch_messages(phone, page)

    def __repr__(self) -> str:
        """
        Return a concise string representation of this distributor.

        Returns
        -------
        str
            A string like 'GSMDistributor(provider=SMS24ME)'.
        """
        return f"GSMDistributor(provider={self.provider_enum.name})"

