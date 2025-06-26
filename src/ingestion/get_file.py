from rich import print as rprint
from requests_cache import CachedSession
from typing import Literal
import json


def get_url_from_endpoints(endpoints_path: str = "src/ingestion/endpoints.json", filetype: Literal["parquet", "json", "csv"] = 'parquet') -> str | None:
    with open(endpoints_path, "r") as file:
        endpoints: dict = json.load(file)
    if filetype not in endpoints.keys():
        rprint(f"filetype '{filetype}' not found in endpoints.json")
        return None
    return endpoints[filetype]


def get_file_from_url(url: str | None, session: CachedSession) -> dict:

    if url is None:
        rprint("[bold red]No URL provided.[/bold red]")
        return {"status": 404, "from_cache": False, "response": None}

    # Explicitly delete expired cache even if the hash is the same
    session.cache.delete(expired=True)

    response = session.get(url)

    return {"status":response.status_code,
            "from_cache":response.from_cache,
            "response": response.content}
