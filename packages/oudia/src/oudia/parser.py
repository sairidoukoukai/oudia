from typing import TextIO

from oudia.nodes.node import EntryList, NodeList
from .nodes import (
    type_to_typed_node_type,
    Node,
    TypedNode,
    OuDia,
)

import logging

logger = logging.getLogger(__name__)


def parse(text: str) -> Node | None:
    stack: list[Node] = []
    current = None

    for line in text.splitlines():
        if not line:
            continue

        if "=" not in line:
            line = line.strip()  # to prevent stupid human error
        else:
            line = line.lstrip()  # to allow indented for debug

        if line.endswith("."):
            if line != ".":
                # `Node.`` (start of node)
                node_type = line[:-1]
                new_node = Node(node_type, EntryList())

                if current is not None:
                    stack.append(current)

                current = new_node
            elif current and stack:
                # `.` (end of node)
                parent = stack.pop()

                found = False
                for child in parent.entries:
                    if isinstance(child, NodeList) and child and child[0].type == current.type:
                        child.append(current)
                        found = True
                        break
                if not found:
                    parent.entries.append(NodeList(Node, [current]))
                current = parent

        elif "=" in line:
            # `Key=Value` (property)
            key, value = line.split("=", 1)
            if current:
                current.entries.append((key, value))

    if current:
        for i, child in enumerate(current.entries):
            if isinstance(child, list) and len(child) == 1:
                current.entries[i] = NodeList(Node, [child[0]])

    return current


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

    try:
        file_type = text.split("\n")[0].split("=", 1)[1]
        if not file_type.startswith("OuDia"):
            raise ValueError()
    except Exception:
        logger.warning(
            'Unsupported file format: "%s", some features may not work correctly.',
            file_type,
        )

    root = replace_node(parse(f"Root.\n{text.strip()}\n."))

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
