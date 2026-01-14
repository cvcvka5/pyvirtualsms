"""
Public package interface for pyvirtualsms.

This module exposes the high-level API that most users should interact with:
    - GSMDistributor: main entry point for working with SMS providers.
    - Provider: enum of supported providers.
    - Country, Phone, Message: simple typed structures describing provider data.
"""

from .distributor import GSMDistributor
from .models import Provider, Country, Phone, Message

__all__ = ["GSMDistributor", "Provider", "Country", "Phone", "Message"]
