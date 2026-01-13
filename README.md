<p align="center">
<img src="/assets/banner.jpg">
</p>

# pyvirtualsms

A small, focused Python library for scraping temporary SMS inboxes. Built for developers who want a clean API, predictable behavior, and zero nonsense.

This started as a personal tool for automating SMS verification flows during scraping. It grew into something reusable, so now it lives here. The goal is simple: provide a lightweight, provider‑agnostic interface for fetching countries, numbers, and messages from virtual SMS services.

## Features

- Minimal, readable codebase
- Provider‑agnostic architecture
- Multi-provider support
- Randomized headers to mimic basic browser behavior
- Structured responses for countries, numbers, and messages
- Only depends on requests and selectolax

## Installation

```bash
pip install pyvirtualsms
```

Or, if you're working with the repo directly:

```bash
pip install -e .
```

## Quick start

```python
from pyvirtualsms import GSMDistributor, Provider

dist = GSMDistributor(Provider.SMS24ME)

# Get a random number from a random country
phone = dist.get_random_number()
print("Using number:", phone)

# Fetch messages from page 1
messages = dist.get_messages(phone, page=1)
for msg in messages:
    print(msg["sender"], ":", msg["text"])
```

## Basic usage

### Get available countries

```python
countries = dist.get_countries()
for country in countries:
print(country["name"], "-", country["url"])
```

### Get numbers for a specific country

```python
country = countries[0]
numbers = dist.get_numbers(country=country)

for num in numbers:
    print(num["number"], "-", num["url"])
```

### Fetch messages for a number

```python
phone = dist.get_random_number()
messages = dist.get_messages(phone, page=1)

for msg in messages:
    print(f"[{msg['sender']}] {msg['text']}")
```

## Project structure

```text
pyvirtualsms/
│
├── client.py                    # HTTP utilities and headers
├── models.py                    # TypedDicts and enums
├── provider_base.py   # Abstract provider interface
├── sms24me.py                  # SMS24.me  implementation
└── distributor.py          # High-level public API
```

## Why this exists

Most temporary SMS tools are either over‑engineered, tied to one provider, or abandoned. This project aims to be simple enough to understand, flexible enough to extend, and stable enough for automation.

## Contributing

Open an issue or PR if you'd like to add a provider, fix a bug, or improve parsing.

## License

MIT License.
