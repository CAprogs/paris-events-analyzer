"""Main ingestion workflow for downloading and storing source data."""

import os
from datetime import timedelta
from io import BytesIO

from minio import Minio
from requests_cache import CachedSession
from src.logger import log

from .get_file import FileType, get_file_from_url, get_url_from_endpoints
from .write_to_storage import write_to_storage


def ingest(
    client: Minio,
    session: CachedSession,
    endpoints_path: str = "src/ingestion/endpoints.json",
    filetype: FileType = "parquet",
) -> bool | None:
    """Run the ingestion pipeline from endpoint lookup to object storage."""
    # Get the URL from endpoints.json
    url = get_url_from_endpoints(endpoints_path=endpoints_path, filetype=filetype)

    # Load the parquet file in memory
    response = get_file_from_url(url=url, session=session)

    log.info("Response status: %s, from cache: %s", response["status"], response["from_cache"])

    if response["response"] is None:
        log.error("No file content was returned by the source endpoint.")
        return False

    data = BytesIO(response["response"])

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
        log.info("Ingestion completed successfully.")
    elif result is False:
        log.error("Ingestion failed.")
    else:
        log.warning("Ingestion skipped: file already exists.")
