"""Utilities to resolve ingestion endpoints and download source files."""

from requests_cache import CachedSession
from typing import Literal
import json

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()], markup=True)
log = logging.getLogger("rich")


def get_url_from_endpoints(
    endpoints_path: str = "src/ingestion/endpoints.json", filetype: Literal["parquet", "json", "csv"] = "parquet"
) -> str | None:
    """Return the endpoint URL for a given file type from the endpoints file.

    Args:
        endpoints_path: Path to the JSON file containing endpoint URLs by file type.
        filetype: Expected output format key to resolve.

    Returns:
        The URL associated with filetype, or None when the key is missing.
    """
    with open(endpoints_path) as file:
        endpoints: dict = json.load(file)
    if filetype not in endpoints.keys():
        log.error(f"filetype '{filetype}' not found in endpoints.json")
        return None
    return endpoints[filetype]


def get_file_from_url(url: str | None, session: CachedSession) -> dict:
    """Download file content from a URL using the provided cached session.

    Args:
        url: Source URL to fetch.
        session: requests-cache session used to perform the HTTP request.

    Returns:
        A dictionary containing response status, cache origin, and binary payload.
        If url is None, returns a default not-found response payload.
    """
    if url is None:
        log.error("[bold red]No URL provided.[/bold red]")
        return {"status": 404, "from_cache": False, "response": None}

    # Explicitly delete expired cache even if the hash is the same
    session.cache.delete(expired=True)

    response = session.get(url)

    return {"status": response.status_code, "from_cache": response.from_cache, "response": response.content}
