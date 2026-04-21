"""Module for writing data to a Minio storage bucket."""

from minio import Minio
from minio.error import S3Error
from logger.log_handler import log
from datetime import datetime, timedelta
from typing import Literal
from io import BytesIO


def today_date() -> str:
    """Returns the current date in 'YYYY-MM-DD' format."""
    return datetime.now().strftime("%Y-%m-%d")


def day_before_date() -> str:
    """Returns the date of the previous day in 'YYYY-MM-DD' format."""
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def write_to_storage(
    client: Minio, data: BytesIO, filetype: Literal["parquet", "json", "csv"] = "parquet"
) -> bool | None:
    """Writes data to a Minio bucket based on the current time and file type."""
    try:
        if not client.bucket_exists(filetype):
            log.error(f"Bucket '{filetype}' does not exist. Please check your Docker setup.")
            return False

        if datetime.now().hour >= 9:
            filename = f"{today_date()}_data.{filetype}"
        else:
            filename = f"{day_before_date()}_data.{filetype}"

        objects = client.list_objects(bucket_name=filetype, prefix=filename)
        if any(objects):
            log.warning(f"Object '{filename}' already exists in bucket '{filetype}'.")
            return None

        result = client.put_object(filetype, filename, data, length=-1, part_size=5 * 1024 * 1024)

        log.info(f"Created {result.object_name} object; etag: {result.etag}, version-id: {result.version_id}")
        return True
    except S3Error as e:
        log.error("An error occurred.", e)
        return False
