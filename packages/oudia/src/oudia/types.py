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

        return f"{self.type}.\n{attributes}\n{children}."

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


@dataclass
class Eki(TypedNode):
    """駅"""

    ekimei: str
    """駅名"""

    ekijikokukeisiki: str
    """駅時刻形式"""

    ekikibo: str
    """駅規模"""

    _children: list["Node | TypedNode"] = field(default_factory=list)

    @property
    def children(self) -> list["Node | TypedNode"]:
        return self._children

    @staticmethod
    def from_node(node: Node) -> "Eki":
        return Eki(
            ekimei=node.attributes["Ekimei"],
            ekijikokukeisiki=node.attributes["Ekijikokukeisiki"],
            ekikibo=node.attributes["Ekikibo"],
        )

    def to_node(self) -> Node:
        return Node(
            type="Eki",
            attributes={
                "Ekimei": self.ekimei,
                "Ekijikokukeisiki": self.ekijikokukeisiki,
                "Ekikibo": self.ekikibo,
            },
        )


def snake_case_to_CamelCase(snake_case: str) -> str:
    return "".join(word.title() for word in snake_case.split("_"))


@dataclass
class Rosen(TypedNode):
    """路線"""

    rosenmei: str
    """路線名"""

    kudari_dia_alias: str | None = None
    """下りダイア別名（OuDiaSecond.1.04+）"""

    nobori_dia_alias: str | None = None
    """上りダイア別名（OuDiaSecond.1.04+）"""

    kiten_jikoku: str | None = None
    """起点時刻"""

    diagram_dgr_y_zahyou_kyori_default: int | None = None
    """ダイヤグラムDGRY座標距離デフォルト"""

    comment: str | None = None
    """コメント"""

    _children: list["Node | TypedNode"] = field(
        default_factory=list,
    )

    @property
    def children(self) -> list["Node | TypedNode"]:
        return self._children

    @staticmethod
    def from_node(node: Node) -> "Rosen":
        return Rosen(
            rosenmei=node.attributes["Rosenmei"],
            kudari_dia_alias=node.attributes.get("KudariDiaAlias"),
            nobori_dia_alias=node.attributes.get("NoboriDiaAlias"),
            kiten_jikoku=node.attributes.get("KitenJikoku"),
            diagram_dgr_y_zahyou_kyori_default=(
                int(v)
                if (v := node.attributes.get("DiagramDgrYZahyouKyoriDefault"))
                else None
            ),
            comment=node.attributes.get("Comment"),
            _children=node.children,
        )

    def to_node(self) -> Node:
        return Node(
            type="Rosen",
            attributes={
                snake_case_to_CamelCase(k): v
                for k, v in self.__dict__.items()
                if k != "_children" and v
            },
            children=self.children,
        )

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Node):
            return self.to_node() == value
        if isinstance(value, Rosen):
            return self.rosenmei == value.rosenmei and self.children == value.children
        return False
