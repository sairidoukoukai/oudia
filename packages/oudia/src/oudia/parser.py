from typing import Iterator, TextIO

from oudia.nodes.node import Attributes, Children
from oudia.nodes.track import EkiTrack2, EkiTrack2Cont
from .nodes import (
    Eki,
    Rosen,
    Node,
    TypedNode,
    OuDia,
    FileType,
    Ressyasyubetsu,
    DispProp,
)
from typing import Annotated

import logging

logger = logging.getLogger(__name__)


def parse(lines: list[str]) -> Iterator[Node]:
    stack: list[Node] = []
    current_node: Node | None = None

    is_trailing: Annotated[bool, "hello"] = False
    """This decides if children list is already read or not"""

    for line in lines:
        line = line.strip()
        if line.endswith("."):
            if line != ".":
                # Block.
                new_node = Node(
                    line[:-1],
                    attributes=Attributes(),
                    children=Children(),
                    trailing_attributes=Attributes(),
                )
                if current_node:
                    stack.append(current_node)
                current_node = new_node
                is_trailing = False
            elif current_node:
                # .
                if stack:
                    parent = stack.pop()
                    parent.add_child(current_node)
                    current_node = parent
                    is_trailing = True
                else:
                    yield current_node
                    current_node = None
                    is_trailing = False

        elif "=" in line:
            # Key=Value
            key, value = line.split("=", 1)
            if current_node:
                if is_trailing:
                    current_node.trailing_attributes.append((key, value))
                else:
                    current_node.attributes.append((key, value))

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

    nodes = list(parse(f"Root.\n{text.strip()}\n.".splitlines()))

    # replace node with typednode by type recursively
    def replace_node(node) -> Node | TypedNode:
        assert isinstance(node, Node)
        # if not isinstance(node, Node):
        #     return node

        replaced_children = Children([replace_node(child) for child in node.children])
        new_node = Node(
            node.type, node.attributes, replaced_children, node.trailing_attributes
        )

        match node.type:
            case "Root":
                new_node = OuDia.from_node(new_node)
            case "Rosen":
                new_node = Rosen.from_node(new_node)
            case "Eki":
                new_node = Eki.from_node(new_node)
            case "Ressyasyubetsu":
                new_node = Ressyasyubetsu.from_node(new_node)
            case "EkiTrack2":
                new_node = EkiTrack2.from_node(new_node)
            case "EkiTrack2Cont":
                new_node = EkiTrack2Cont.from_node(new_node)
            case "DispProp":
                new_node = DispProp.from_node(new_node)
            case _:
                pass

        return new_node

    print(f"{nodes[0]=}")
    root = replace_node(nodes[0])
    assert isinstance(root, OuDia)
    print(f"{root=}")
    print(f"{root.file_type_app_comment=}")
    return root


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
