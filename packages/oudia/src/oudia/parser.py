from typing import Iterator, TextIO
from .types import OuDia, FileType, Node, TypedNode
from .nodes import Eki, Rosen

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
    # ignore bom
    if text.startswith("\ufeff"):
        text = text[1:]

    if not text.startswith("FileType="):
        raise ValueError(
            f"Invalid file type, starting bytes are not 'FileType=': {text[:10]}"
        )

    file_type = FileType.from_str(text.split("\n")[0].split("=", 1)[1])
    if file_type.software not in ["OuDia", "OuDiaSecond"]:
        logger.warning(
            'Unsupported software: "%s", some features may not work correctly.',
            file_type.software,
        )

    aftermath = text.split("\n.\n")[-1] if "\n.\n" in text else None
    aftermath_line_count = aftermath.count("\n") if aftermath else 0

    nodes = list(parse(text.splitlines()[1 : -aftermath_line_count - 1]))

    # replace node with typednode by type recursively
    def replace_node(node) -> Node | TypedNode:
        if not isinstance(node, Node):
            return node

        new_node = Node(node.type, node.attributes)
        new_node.children = [replace_node(child) for child in node.children]

        match node.type:
            case "Rosen":
                new_node = Rosen.from_node(new_node)
            case "Eki":
                new_node = Eki.from_node(new_node)
            case _:
                pass

        return new_node

    nodes: list[TypedNode | Node] = [replace_node(node) for node in nodes]

    return OuDia(file_type, nodes, aftermath=aftermath)


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
