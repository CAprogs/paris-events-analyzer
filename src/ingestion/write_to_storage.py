"""Helpers for writing ingested data files to MinIO object storage."""

from minio import Minio
from minio.error import S3Error
import logging
from rich.logging import RichHandler
from datetime import datetime, timedelta
from typing import Literal
from io import BytesIO

logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
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
    """Write data to the appropriate MinIO bucket, skipping if the object already exists."""
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
            log.warning(f"Object '{filename}' already exists in bucket '{filetype}'.")
            return None

        # Upload and save the object
        # Here, 'data' is expected to be a bytes-like object
        result = client.put_object(filetype, filename, data, length=-1, part_size=5 * 1024 * 1024)

        log.info(f"Created '{result.object_name}' object; etag: '{result.etag}', version-id: '{result.version_id}'")
        return True
    except S3Error as e:
        log.error("An error occurred.", e)
        return False
