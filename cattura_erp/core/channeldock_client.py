"""Simple ChannelDock API client skeleton.

This module abstracts the external API so that other modules interact with a
clean Python interface. The actual HTTP integration can be filled in later.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List


DEFAULT_BASE_URL = "https://api.channeldock.com/v1"


@dataclass
class ChannelDockConfig:
    api_key: str
    base_url: str = DEFAULT_BASE_URL


class ChannelDockClient:
    def __init__(self, config: ChannelDockConfig):
        self.config = config

    def fetch_products(self) -> List[Dict[str, Any]]:
        """Return a list of product payloads.

        Replace the NotImplementedError with HTTP calls that map the
        ChannelDock response into simple dictionaries.
        """

        raise NotImplementedError("Implement ChannelDock API call")

    def fetch_inventory(self) -> List[Dict[str, Any]]:
        """Return inventory information for products."""

        raise NotImplementedError

    def fetch_orders(self, since: str | None = None) -> Iterable[Dict[str, Any]]:
        """Return orders created/updated since the provided ISO date string."""

        raise NotImplementedError


def get_client(api_key: str, base_url: str | None = None) -> ChannelDockClient:
    return ChannelDockClient(ChannelDockConfig(api_key=api_key, base_url=base_url or DEFAULT_BASE_URL))
