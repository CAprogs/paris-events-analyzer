"""Rich-backed logging configuration for the project."""

import logging

from rich.logging import RichHandler


def build_logger() -> logging.Logger:
    """Create and return the shared application logger."""
    logger = logging.getLogger("paris-events-analyzer")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = RichHandler(markup=True, rich_tracebacks=True, show_path=False)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(handler)
    logger.propagate = False
    return logger
