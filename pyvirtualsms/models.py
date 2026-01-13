from enum import Enum
from typing import TypedDict, List, Optional


class Provider(Enum):
    SMS24ME = "https://sms24.me"


class Country(TypedDict):
    name: str
    url: str


class Phone(TypedDict):
    number: str
    url: str


class Message(TypedDict):
    sender: str
    text: str

