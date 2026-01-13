from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Country, Phone, Message


class SMSProvider(ABC):
    """Abstract base class for SMS providers."""

    @abstractmethod
    def fetch_countries(self) -> List[Country]:
        pass

    @abstractmethod
    def fetch_numbers(self, country: Optional[Country] = None) -> List[Phone]:
        pass

    @abstractmethod
    def fetch_messages(self, phone: Phone, page: int = 1) -> List[Message]:
        pass

