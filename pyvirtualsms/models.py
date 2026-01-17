"""
Core data models for pyvirtualsms.

This module defines simple typed structures to describe:
    - Provider: supported SMS providers.
    - Country: metadata about a provider's country entry.
    - Phone: a phone number entry belonging to a country.
    - Message: an individual SMS message.
"""

from enum import Enum
from typing import TypedDict


class Provider(Enum):
    """
    Enumeration of supported SMS providers.

    Each value stores the base URL for the provider's website.
    """

    SMS24ME = "https://sms24.me"
    RECEIVESMSS = "https://receive-smss.com"
    FREEPHONENUM = "https://freephonenum.com"


class Country(TypedDict):
    """
    Representation of a country as returned by a provider.

    Keys
    ----
    name : str
        Human-readable country name (e.g. "Austria").
    url : str
        Provider-specific URL or path identifying the country.
    """

    name: str
    url: str


class Phone(TypedDict):
    """
    Representation of a phone number entry.

    Keys
    ----
    number : str
        The phone number as a string.
    url : str
        Provider-specific URL or path pointing to the phone's detail/messages page.
    country : Country
        The country this phone belongs to.
    """

    number: str
    url: str
    country: Country


class Message(TypedDict):
    """
    Representation of a single SMS message.

    Keys
    ----
    sender : str
        The sender information as displayed by the provider.
    text : str
        The message body/content.
    """

    sender: str
    text: str

