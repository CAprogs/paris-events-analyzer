"""Main module for ingesting data into MinIO storage."""

from logger.log_handler import log
from write_to_storage import write_to_storage
from get_file import get_file_from_url, get_url_from_endpoints
from requests_cache import CachedSession
from datetime import timedelta
from minio import Minio
from io import BytesIO
import os


def ingest(
    client: Minio,
    session: CachedSession,
    endpoints_path: str = "src/ingestion/endpoints.json",
    filetype: str = "parquet",
) -> bool | None:
    """Ingests data from a specified URL into a MinIO storage bucket."""
    url = get_url_from_endpoints(endpoints_path=endpoints_path, filetype=filetype)

    response = get_file_from_url(url=url, session=session)

    log.info(f"Response status: {response['status']}, From cache: {response['from_cache']}")

    data = BytesIO(response["response"])

    result = write_to_storage(client=client, data=data, filetype=filetype)

    return result


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(".env")

    client = Minio(
        endpoint="localhost:9000",
        access_key=os.getenv("DBT_ENV_SECRET_MINIO_ACCESS_KEY"),
        secret_key=os.getenv("DBT_ENV_SECRET_MINIO_SECRET_KEY"),
        secure=False,
    )

    session = CachedSession(cache_name="pea_cache", backend="filesystem", expire_after=timedelta(days=1))

    result = ingest(client=client, session=session)

    if result is True:
        log.info("Ingestion completed successfully.")
    elif result is False:
        log.error("Ingestion failed.")
    else:
        log.warning("Ingestion skipped: file already exists.")
