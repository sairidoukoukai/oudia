from dataclasses import dataclass, field
from abc import ABC, abstractmethod


class Attributes(list[tuple[str, str]]):
    def __init__(self, *args: tuple[str, str | None]) -> None:
        super().__init__([(k, v) for k, v in args if v is not None])

    # def __new__(cls, x) -> "Attributes":
    #     return super(Attributes, cls).__new__(X)

    def __str__(self) -> str:
        return "\n".join([f"{key}={value}" for key, value in self])

    def __repr__(self) -> str:
        return f"Attributes({', '.join(str(pair) for pair in self)})"

    def get(self, key: str) -> str | None:
        for k, v in self:
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


class Children(list["Node | TypedNode"]):
    def __str__(self) -> str:
        return "\n".join([str(child) for child in self])

    def __repr__(self) -> str:
        return f"Children({super().__repr__()})"


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
    attributes: Attributes
    children: Children
    trailing_attributes: Attributes

    def add_child(self, node: "Node"):
        """
        Adds a child to the node.

        Args:
            node (Node): The node to add.
        """
        self.children.append(node)

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
                self.attributes,
                self.children,
                self.trailing_attributes,
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
            return (
                self.type == value.type
                and self.attributes == value.attributes
                and self.children == value.children
            )

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
        for key, value in self.attributes:
            print(" " * (indent + 2) + f"{key}={value}")
        for child in self.children:
            child.pprint(indent + 2)
        for key, value in self.trailing_attributes:
            print(" " * (indent + 2) + f"{key}={value}")
        if self.type:
            print(" " * indent + ".")


@dataclass
class TypedNode(ABC):
    """
    An abstract class representing a typed node.
    """

    @property
    @abstractmethod
    def children(self) -> list["Node | TypedNode"]:
        """
        Returns the children of the node.

        Returns:
            list[Node | TypedNode]: The children of the node.
        """
        pass

    @abstractmethod
    def to_node(self) -> Node:
        """
        Returns the node as a `Node` object.

        Returns:
            Node: The node as a `Node` object.
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
