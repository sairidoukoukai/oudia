from typing import Iterator, TextIO, Type

from oudia.nodes.node import EntryList, NodeList
from .nodes import (
    TYPE_TO_NODE,
    Node,
    TypedNode,
    OuDia,
    FileType,
)

import logging

logger = logging.getLogger(__name__)


def type_to_typed_node_type(type: str | None) -> Type[TypedNode] | None:
    return TYPE_TO_NODE.get(type) if type else None


def parse(text: str) -> Iterator[Node]:
    stack: list[Node] = []
    current_node: Node | None = None

    for line in text.splitlines():
        if line.endswith("."):
            if line != ".":
                # Block.
                new_node = Node(
                    line[:-1],
                    entries=EntryList(),
                )
                if current_node:
                    stack.append(current_node)
                current_node = new_node
            elif current_node:
                # .
                if stack:
                    parent = stack.pop()
                    # add to last node list if

                    current_typed_node_type = type_to_typed_node_type(current_node.type) or Node

                    if (
                        parent.entries.node_lists
                        and parent.entries.node_lists[-1]
                        and parent.entries.node_lists[-1].type is current_typed_node_type
                    ):
                        parent.entries.node_lists[-1].append(current_node)
                    else:
                        parent.entries.append(NodeList(current_typed_node_type, [current_node]))

                    current_node = parent
                else:
                    yield current_node
                    current_node = None

        elif "=" in line:
            # Key=Value
            key, value = line.split("=", 1)
            if current_node:
                current_node.entries.append((key, value))

    if current_node:
        yield current_node


def replace_node_list(node_list: NodeList) -> NodeList:
    nodes = [replace_node(child) for child in node_list]
    first_node_type = type(nodes[0]) if nodes else Node

    return NodeList(first_node_type, nodes)


def replace_nodes_in_entry_list(entry_list: EntryList) -> EntryList:
    result = EntryList()
    for entry in entry_list:
        if isinstance(entry, NodeList):
            result.append(replace_node_list(entry))
        else:
            result.append(entry)
    return result


def replace_node(node) -> Node | TypedNode:
    """Recursively replace `Node` with `TypedNode` by `type`."""

    assert isinstance(node, Node)
    # if not isinstance(node, Node):
    #     return node

    new_node = Node(
        node.type,
        entries=replace_nodes_in_entry_list(node.entries),
    )

    # replaced_children = NodeList([replace_node(child) for child in node.children])

    CurrentType: type[TypedNode] | None = type_to_typed_node_type(node.type) if node.type else None

    if CurrentType:
        new_node = CurrentType.from_node(new_node)
    else:
        logger.warning(f"Unsupported node type: {node.type}")

    return new_node


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
        raise ValueError(f"Invalid file type, starting bytes are not 'FileType=': {text[:10]}")

    file_type = FileType.from_str(text.split("\n")[0].split("=", 1)[1])
    if file_type.software not in ["OuDia", "OuDiaSecond"]:
        logger.warning(
            'Unsupported software: "%s", some features may not work correctly.',
            file_type.software,
        )

    nodes = list(parse(f"Root.\n{text.strip()}\n."))

    # print(f"{nodes[0]=}")
    root = replace_node(nodes[0])
    assert isinstance(root, OuDia)
    # print(f"{root=}")
    # print(f"{root.file_type_app_comment=}")
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
