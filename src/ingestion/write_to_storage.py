from minio import Minio
from minio.error import S3Error
from rich import print as rprint
from datetime import datetime, timedelta
from typing import Literal
from io import BytesIO


def today_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def day_before_date() -> str:
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

def write_to_storage(client: Minio, data: BytesIO, filetype: Literal["parquet", "json", "csv"] = "parquet") -> bool | None:
    try:
        # Check if the bucket exists
        if not client.bucket_exists(filetype):
            rprint(f"Bucket '{filetype}' does not exist. Please check your Docker setup.")
            return False

        # Create a filename with the current date if it's 9am or later
        if datetime.now().hour >= 9:
            filename = f"{today_date()}_data.{filetype}"
        else:
            filename = f"{day_before_date()}_data.{filetype}"

        # Check if the object already exists
        objects = client.list_objects(bucket_name=filetype, prefix=filename)
        if any(objects):
            rprint(f"Object [bold blue]'{filename}'[/bold blue] already exists in bucket [bold yellow]'{filetype}'[/bold yellow].")
            return None

        # Upload and save the object
        # Here, 'data' is expected to be a bytes-like object
        result = client.put_object(filetype, filename, data, length=-1, part_size=5*1024*1024)

        rprint(
            "Created [bold blue]{0}[/bold blue] object; etag: [bold red]{1}[/bold red], version-id: [bold magenta]{2}[/bold magenta]".format(
            result.object_name, result.etag, result.version_id,
            ),
               )
        return True
    except S3Error as e:
        rprint("An error occurred.", e)
        return False
