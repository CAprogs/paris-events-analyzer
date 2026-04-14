"""Helpers for reading dataset URLs and fetching remote files."""

import json

from requests_cache import CachedSession
from src.logger import log
from typing import Literal


def get_url_from_endpoints(
    endpoints_path: str = "src/ingestion/endpoints.json", filetype: Literal["parquet", "json", "csv"] = "parquet"
) -> str | None:
    """Return the configured source URL for a given file type."""
    with open(endpoints_path) as file:
        endpoints: dict = json.load(file)
    if filetype not in endpoints.keys():
        log.warning(f"filetype '{filetype}' not found in endpoints.json")
        return None
    return endpoints[filetype]


def get_file_from_url(url: str | None, session: CachedSession) -> dict:
    """Download a remote file and return its payload with cache metadata."""
    if url is None:
        log.error("No URL provided.")
        return {"status": 404, "from_cache": False, "response": None}

    # Explicitly delete expired cache even if the hash is the same
    try:
        session.cache.delete(expired=True)
    except Exception as error:
        log.warning("Cache cleanup failed, clearing the whole cache instead: %s", error)
        session.cache.clear()

    response = session.get(url)

    return {"status": response.status_code, "from_cache": response.from_cache, "response": response.content}
