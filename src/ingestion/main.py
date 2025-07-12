from rich import print as rprint
from write_to_storage import write_to_storage
from get_file import get_file_from_url, get_url_from_endpoints
from requests_cache import CachedSession
from datetime import timedelta
from minio import Minio
from io import BytesIO
import os


def ingest(client: Minio, session: CachedSession, endpoints_path: str = "src/ingestion/endpoints.json", filetype: str = "parquet") -> bool | None:

    # Get the URL from endpoints.json
    url = get_url_from_endpoints(endpoints_path=endpoints_path,
                                 filetype=filetype)

    # Load the parquet file in memory
    response = get_file_from_url(
        url=url,
        session=session,
    )

    rprint(f"Response status: {response['status']}, From cache: {response['from_cache']}")

    data = BytesIO(response["response"])

    # Try to write the data to MinIO storage
    result = write_to_storage(client=client,
                            data=data,
                            filetype=filetype
                            )

    return result


if __name__ == "__main__":

    from dotenv import load_dotenv

    load_dotenv(".env")

    # Create a MinIO client instance
    client = Minio(endpoint="localhost:9000",
                access_key=os.getenv("DBT_ENV_SECRET_MINIO_ACCESS_KEY"),
                secret_key=os.getenv("DBT_ENV_SECRET_MINIO_SECRET_KEY"),
                secure=False  # not using HTTPS for local development
            )

    # Create a reusable requests session with caching
    session = CachedSession(cache_name="pea_cache", backend="filesystem", expire_after=timedelta(days=1))

    result = ingest(client=client, session=session)

    if result is True:
        rprint("[bold green]Ingestion completed successfully.[/bold green]")
    elif result is False:
        rprint("[bold red]Ingestion failed.[/bold red]")
    else:
        rprint("[bold yellow]Ingestion skipped: file already exists.[/bold yellow]")

