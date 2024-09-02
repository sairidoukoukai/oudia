from typing import Iterator, TextIO
from .types import OuDia, FileType, Node

import logging
logger = logging.getLogger(__name__)
def parse(lines: list[str]) -> Iterator[Node]:
    stack: list[Node] = []
    current_node: Node | None = None
    
    for line in lines:
        line = line.strip()
        if line.endswith("."):
            if line != ".":
                # Block.
                new_node = Node(line[:-1])
                if current_node:
                    stack.append(current_node)
                current_node = new_node
            elif current_node:
                # .
                if stack:
                    parent = stack.pop()
                    parent.add_child(current_node)
                    current_node = parent
                else:
                    yield current_node
                    current_node = None

        elif "=" in line:
            # Key=Value
            key, value = line.split("=", 1)
            if current_node:
                current_node.attributes[key] = value
    
    if current_node:
        yield current_node


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

    return OuDia(file_type, list(parse(text.splitlines()[1:])))

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