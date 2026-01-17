"""
HTTP client utilities for pyvirtualsms.

This module provides a small wrapper around `requests` that:
    - Randomizes User-Agent and language headers to resemble real browsers.
    - Applies a default timeout.
    - Raises clear, high-level errors for HTTP failures.
"""

import random
import requests

# A small pool of realistic User-Agent strings to mimic real browsers.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/121.0",
]

# Language headers to simulate different locales.
LANG_HEADERS = [
    "en-US,en;q=0.9",
    "de-DE,de;q=0.9",
    "en-GB,en;q=0.8",
]


def build_human_headers() -> dict:
    """
    Build a set of HTTP headers that look like they come from a browser.

    Returns
    -------
    dict
        A dictionary with randomized User-Agent and Accept-Language headers,
        plus a few other browser-like defaults.
    """
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": random.choice(LANG_HEADERS),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        ),
        "Connection": "keep-alive",
        "DNT": str(random.choice([0, 1])),
        "Upgrade-Insecure-Requests": "1",
    }


def human_get(url: str) -> requests.Response:
    """
    Perform an HTTP GET request with randomized browser-like headers.

    This function:
        - Applies a default timeout of 10 seconds.
        - Raises a RuntimeError if any network or HTTP error occurs.

    Parameters
    ----------
    url : str
        The URL to fetch.

    Returns
    -------
    requests.Response
        The HTTP response object with a successful (2xx) status code.

    Raises
    ------
    RuntimeError
        If the request fails or a non-success status code is returned.
    """
    try:
        # Perform the request with realistic headers and a sane timeout.
        resp = requests.get(url, headers=build_human_headers(), timeout=20)
        resp.raise_for_status()
        return resp
    except requests.RequestException as e:
        # Surface a simple, high-level error instead of raw requests exceptions.
        raise RuntimeError(f"HTTP error while fetching {url}: {e}")

