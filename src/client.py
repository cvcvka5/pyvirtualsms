import random
import requests

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/121.0"
]

LANG_HEADERS = [
    "en-US,en;q=0.9",
    "de-DE,de;q=0.9",
    "en-GB,en;q=0.8"
]


def build_human_headers() -> dict:
    """Return randomized HTTP headers to mimic real browser traffic."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": random.choice(LANG_HEADERS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
        "DNT": str(random.choice([0, 1])),
        "Upgrade-Insecure-Requests": "1",
    }


def human_get(url: str) -> requests.Response:
    """Perform a GET request with randomized headers."""
    return requests.get(url, headers=build_human_headers(), timeout=10)

