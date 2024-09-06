from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

T = TypeVar("T", bound="Node | TypedNode")


class NodeList[T](list[T]):
    type: Type[T]

    def __init__(self, type: Type[T], args: list[T] | None = None) -> None:
        super().__init__(args if args is not None else [])
        self.type = type

    def __str__(self) -> str:
        assert all(bool(child) for child in self)
        return "\n".join([str(child) for child in self])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.type.__name__}, {super().__repr__()})"


Property = tuple[str, str]
# NodeList = list["Node | TypedNode"]
Entry = Property | NodeList


class EntryList(list[Property | NodeList]):

    @staticmethod
    def parse_value(value: str | int | bool | None) -> str:
        if value is None:
            return ""
        if isinstance(value, bool):
            return "1" if value else "0"
        return str(value)

    # def __init__(self, *args: tuple[str, str | int | bool | None]) -> None:

    @staticmethod
    def parse_item(value: tuple[str | None, str | int | bool | NodeList | None]) -> Entry:
        k, v = value
        if k is not None and isinstance(v, NodeList):
            raise ValueError("NodeList cannnot have key")
        if isinstance(v, NodeList):
            return v
        if k is None:
            raise ValueError("Key must be specified for properties")
        return (k, EntryList.parse_value(v))

    # def __new__(cls, x) -> "Attributes":
    #     return super(Attributes, cls).__new__(X)
    def __init__(self, *args: tuple[str | None, str | int | bool | None | NodeList]) -> None:
        super().__init__([self.parse_item((k, v)) for k, v in args if v is not None])

        # entries: Property

        # super().__init__([(k, self.parse_value(v)) if k else v for k, v in args if v is not None])

    def __str__(self) -> str:
        result = ""

        def format_entry(entry: Property | NodeList) -> str:
            if isinstance(entry, tuple):
                return f"{entry[0]}={entry[1]}"
            if isinstance(entry, NodeList):
                return str(entry)
            raise ValueError(f"Unexpected entry type: {type(entry)}")

        return "\n".join(format_entry(entry) for entry in self if entry)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(repr(pair) for pair in self)})"

    @property
    def properties(self) -> list[Property]:
        return [p for p in self if isinstance(p, tuple)]

    @property
    def node_lists(self) -> list[NodeList]:
        return [p for p in self if isinstance(p, NodeList)]

    T = TypeVar("T", bound="TypedNode | Node")

    def get_list(self, key: int, t: Type[T]) -> NodeList[T]:
        if key >= len(self.node_lists):
            return NodeList(t)
        return self.node_lists[key]

    def get_list_by_type(self, t: Type[T]) -> NodeList[T]:
        for node_list in self.node_lists:
            if node_list.type == t:
                return node_list
        return NodeList(t)

    def get(self, key: str) -> str | None:
        for k, v in self.properties:
            if k == key:
                return v
        return None

    def get_bool(self, key: str) -> bool | None:
        value = self.get(key)
        if value is None:
            return None
        return value == "1"

    def get_int(self, key: str) -> int | None:
        value = self.get(key)
        if value is None:
            return None
        return int(value)

    def get_required(self, key: str) -> str:
        value = self.get(key)
        if value is None:
            raise ValueError(f"Required attribute '{key}' not found.")
        return value

    def get_repeatable(self, key: str) -> list[str]:
        return [v for k, v in self.properties if k == key]


@dataclass
class Node:
    """
    Represents a node in an OuDia file.

    Attributes:
        type (str): The type of the node.
        attributes (dict[str, str]): The attributes of the node.
        children (list[Node]): The children of the node.
    """

    type: str | None
    entries: EntryList

    def __str__(self):
        """
        Returns a serialized string representation of the node.

        Returns:
            str: The string representation of the node.
        """

        return "\n".join(
            str(x)
            for x in [
                f"{self.type}." if self.type else None,
                self.entries,
                "." if self.type else None,
            ]
            if x
        )

        # return f"{self.type}.\n{attributes}\n{children}\\n{trailing_attributes}\\n."

    # def __repr__(self) -> str:
    #     """
    #     Returns a canonical string representation of the node.

    #     Returns:
    #         str: The string representation of the node.
    #     """
    #     return f"Node(type={repr(self.type)}, attributes={repr(self.attributes)}, children={repr(self.children)})"

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Node):
            # return super().__eq__(value)
            return self.type == value.type and self.entries == value.entries

        if isinstance(value, TypedNode):
            return value.to_node() == self

        return False

    def pprint(self, indent: int = 0):
        """
        Prints the node in a pretty format.

        Args:
            indent (int, optional): The indentation level. Defaults to 0.
        """
        if self.type:
            print(" " * indent + self.type + ".")
        for entry in self.entries:
            if isinstance(entry, tuple):
                print(" " * (indent + 2) + f"{entry[0]}={entry[1]}")
            if isinstance(entry, NodeList):
                for child in entry:
                    child.pprint(indent + 2)
        if self.type:
            print(" " * indent + ".")


@dataclass
class TypedNode(ABC):
    """
    An abstract class representing a typed node.
    """

    @abstractmethod
    def to_node(self) -> Node:
        """
        Returns the node as a `Node` object.

        Returns:
            Node: The node as a `Node` object.
        """
        pass

    @classmethod
    @abstractmethod
    def from_node(cls, node: Node) -> "TypedNode":
        """
        Creates a typed node from a `Node` object.

        Args:
            node (Node): The node to create the typed node from.

        Returns:
            TypedNode: The typed node.
        """
        pass

    def pprint(self, indent: int = 0):
        """
        Prints the node in a pretty format.

        Args:
            indent (int, optional): The indentation level. Defaults to 0.
        """
        return self.to_node().pprint(indent)

    def __str__(self) -> str:
        return self.to_node().__str__()
