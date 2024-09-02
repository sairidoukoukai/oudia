from typing import TextIO
from .types import OuDia, FileType

import logging
logger = logging.getLogger(__name__)

def loads(text: str) -> OuDia:
    """
    Loads OuDia data from a given text.

    Args:
        text (str): The text to load OuDia data from.

    Returns:
        OuDia: The loaded OuDia data.

    Raises:
        ValueError: If the text is invalid.
    """
    if not text.startswith("FileType="):
        raise ValueError("Invalid file type")
    
    file_type = FileType.from_str(text.split("\n")[0].split("=", 1)[1])
    if file_type.software not in ["OuDia", "OuDiaSecond"]:
        logger.warning("Unsupported software: \"%s\", some features may not work correctly.", file_type.software)

    return OuDia(file_type=file_type)

def load(fp: TextIO) -> OuDia:
    """
    Loads OuDia data from a given file.

    Args:
        fp (TextIO): The file to load OuDia data from.

    Returns:
        OuDia: The loaded OuDia data.

    Raises:
        ValueError: If the file is invalid.
    """
    return loads(fp.read())