from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class FileType:
    """
    Represents a file type.

    Attributes:
        software (str): The software that created the file.
        version (str | None, optional): The version of the software. Defaults to None.
    """

    software: str
    version: str | None = None

    @staticmethod
    def from_str(text: str) -> "FileType":
        """
        Creates a `FileType` object from a given string.

        Args:
            text (str): The string to parse.

        Returns:
            FileType: The parsed `FileType` object.
        """
        return FileType(*text.split(".", 1))

    def __str__(self) -> str:
        """
        Returns a string representation of the `FileType` object.

        Returns:
            str: The string representation of the `FileType` object.
        """
        return f"{self.software}.{self.version}" if self.version else self.software


@dataclass
class Node:
    """
    Represents a node in an OuDia file.

    Attributes:
        type (str): The type of the node.
        attributes (dict[str, str]): The attributes of the node.
        children (list[Node]): The children of the node.
    """

    type: str
    attributes: dict[str, str] = field(default_factory=dict)
    children: list["Node | TypedNode"] = field(default_factory=list)

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
        attributes = "\n".join(
            [f"{key}={value}" for key, value in self.attributes.items()]
        )
        children = "\n".join([str(child) for child in self.children])

        return f"{self.type}.\n{attributes}\n{children}{'\n' if children else ''}."

    def __repr__(self) -> str:
        """
        Returns a canonical string representation of the node.

        Returns:
            str: The string representation of the node.
        """
        return f"Node(type={repr(self.type)}, attributes={repr(self.attributes)}, children={repr(self.children)})"

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
        print(" " * indent + self.type)
        for key, value in self.attributes.items():
            print(" " * (indent + 2) + f"{key}={value}")
        for child in self.children:
            child.pprint(indent + 2)


@dataclass
class OuDia:
    """
    Represents an OuDia file.

    Attributes:
        file_type (FileType): The file type of the OuDia file.
        chilren (list[Node]): The children of the OuDia file.
        aftermath (str | None, optional): The afterward text of the OuDia file. Defaults to None.
    """

    file_type: FileType
    children: list["Node | TypedNode"]
    aftermath: str | None = None

    def pprint(self, indent: int = 0, with_lines: bool = False):
        """
        Prints the OuDia file in a pretty format.

        Args:
            indent (int, optional): The indentation level. Defaults to 0.
        """
        print(
            " " * indent + str(self.file_type)
            if not with_lines
            else "|" * (indent + 1) + str(self.file_type)
        )
        for child in self.children:
            child.pprint(indent + 2)
        if self.aftermath:
            print(" " * indent + self.aftermath)


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
