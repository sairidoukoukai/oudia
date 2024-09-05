from typing import Iterator, TextIO

from oudia.nodes.node import EntryList, NodeList
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

    for line in lines:
        line = line.strip()
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
                is_trailing = False
            elif current_node:
                # .
                if stack:
                    parent = stack.pop()
                    # add to last node list if

                    if (
                        parent.entries.node_lists
                        and parent.entries.node_lists[-1]
                        and parent.entries.node_lists[-1][-1]
                        and parent.entries.node_lists[-1][-1].type == current_node.type
                    ):
                        parent.entries.node_lists[-1].append(current_node)
                    else:
                        parent.entries.append(NodeList([current_node]))

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

    nodes = list(parse(f"Root.\n{text.strip()}\n.".splitlines()))

    # replace node with typednode by type recursively
    def replace_node(node) -> Node | TypedNode:
        assert isinstance(node, Node)
        # if not isinstance(node, Node):
        #     return node

        node.entries

        def replace_node_list(node_list: NodeList) -> NodeList:
            return NodeList([replace_node(child) for child in node_list])

        def replace_nodes_in_entry_list(entry_list: EntryList) -> EntryList:
            result = EntryList()
            for entry in entry_list:
                if isinstance(entry, NodeList):
                    result.append(replace_node_list(entry))
                else:
                    result.append(entry)
            return result

        new_node = Node(
            node.type,
            entries=replace_nodes_in_entry_list(node.entries),
        )

        # replaced_children = NodeList([replace_node(child) for child in node.children])

        TYPE_TO_NODE: dict[str, type[TypedNode]] = {
            "Root": OuDia,
            "Rosen": Rosen,
            "Eki": Eki,
            "Ressyasyubetsu": Ressyasyubetsu,
            "EkiTrack2": EkiTrack2,
            "EkiTrack2Cont": EkiTrack2Cont,
            "DispProp": DispProp,
        }

        CurrentType: type[TypedNode] | None = TYPE_TO_NODE.get(node.type) if node.type else None

        if CurrentType:
            new_node = CurrentType.from_node(new_node)
        else:
            logger.warning(f"Unsupported node type: {node.type}")

        return new_node

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
