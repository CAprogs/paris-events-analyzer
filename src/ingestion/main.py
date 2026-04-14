"""Entry point to orchestrate retrieval and storage of Paris events data."""

from write_to_storage import write_to_storage
from get_file import DownloadResponse, FileType, get_file_from_url, get_url_from_endpoints
from requests_cache import CachedSession
from datetime import timedelta
from minio import Minio
from io import BytesIO
from typing import cast
import os

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(markup=True)])
log = logging.getLogger("rich")


def ingest(
    client: Minio,
    session: CachedSession,
    endpoints_path: str = "src/ingestion/endpoints.json",
    filetype: FileType = "parquet",
) -> bool | None:
    """Run the ingestion flow from endpoint lookup to MinIO upload.

    Args:
        client: Initialized MinIO client used for storage operations.
        session: Cached HTTP session used to download remote data.
        endpoints_path: Path to the endpoints JSON configuration file.
        filetype: File type key to resolve and upload.

    Returns:
        True when upload succeeds, False on failure, or None when skipped.
    """
    # Get the URL from endpoints.json
    url = get_url_from_endpoints(endpoints_path=endpoints_path, filetype=filetype)

    # Load the parquet file in memory
    response: DownloadResponse = get_file_from_url(url=url, session=session)

    log.info(f"Response status: {response['status']}, From cache: {response['from_cache']}")

    data = BytesIO(cast(bytes, response["response"]))

    # Try to write the data to MinIO storage
    result = write_to_storage(client=client, data=data, filetype=filetype)

    return result


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(".env")

    # Create a MinIO client instance
    client = Minio(
        endpoint="localhost:9000",
        access_key=os.getenv("DBT_ENV_SECRET_MINIO_ACCESS_KEY"),
        secret_key=os.getenv("DBT_ENV_SECRET_MINIO_SECRET_KEY"),
        secure=False,  # not using HTTPS for local development
    )

    # Create a reusable requests session with caching
    session = CachedSession(cache_name="pea_cache", backend="filesystem", expire_after=timedelta(days=1))

    result = ingest(client=client, session=session)

    if result is True:
        log.info("[bold green]Ingestion completed successfully.[/bold green]")
    elif result is False:
        log.error("[bold red]Ingestion failed.[/bold red]")
    else:
        log.warning("[bold yellow]Ingestion skipped: file already exists.[/bold yellow]")
