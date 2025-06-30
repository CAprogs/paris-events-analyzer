"""A module for setting up a logging handler using Rich for better console output."""

import logging
from rich.logging import RichHandler

FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(markup=True), logging.FileHandler("app.log", encoding="utf-8")],
)

log = logging.getLogger("rich")
