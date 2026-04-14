"""Helpers to persist downloaded data into MinIO buckets."""

from minio import Minio
from minio.error import S3Error
from datetime import datetime, timedelta
from typing import Literal
from io import BytesIO

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()], markup=True)
log = logging.getLogger("rich")


def today_date() -> str:
    """Return today's date formatted as YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def day_before_date() -> str:
    """Return yesterday's date formatted as YYYY-MM-DD."""
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def write_to_storage(
    client: Minio, data: BytesIO, filetype: Literal["parquet", "json", "csv"] = "parquet"
) -> bool | None:
    """Upload in-memory data to MinIO if the destination object does not exist.

    Args:
        client: Initialized MinIO client used for bucket and object operations.
        data: In-memory binary stream to upload.
        filetype: Destination bucket and file extension.

    Returns:
        True on successful upload, False on error, or None if object already exists.
    """
    try:
        # Check if the bucket exists
        if not client.bucket_exists(filetype):
            log.error(f"Bucket '{filetype}' does not exist. Please check your Docker setup.")
            return False

        # Create a filename with the current date if it's 9am or later
        if datetime.now().hour >= 9:
            filename = f"{today_date()}_data.{filetype}"
        else:
            filename = f"{day_before_date()}_data.{filetype}"

        # Check if the object already exists
        objects = client.list_objects(bucket_name=filetype, prefix=filename)
        if any(objects):
            log.warning(
                f"Object [bold blue]'{filename}'[/bold blue] already exists in bucket"
                " [bold yellow]'{filetype}'[/bold yellow]."
            )
            return None

        # Upload and save the object
        # Here, 'data' is expected to be a bytes-like object
        result = client.put_object(filetype, filename, data, length=-1, part_size=5 * 1024 * 1024)

        log.info(
            f"Created [bold blue]{result.object_name}[/bold blue] object; etag: [bold red]{result.etag}[/bold red],"
            " version-id: [bold magenta]{result.version_id}[/bold magenta]"
        )
        return True
    except S3Error as e:
        log.error("An error occurred.", e)
        return False
