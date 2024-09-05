from dataclasses import dataclass, field

from .node import Attributes, Children, Node, TypedNode


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
class OuDia(TypedNode):
    """OuDiaファイル"""

    file_type: FileType
    """ファイル形式"""

    file_type_app_comment: str | None = None
    """ファイル形式のアプリコメント"""

    _children: list["Node | TypedNode"] = field(default_factory=list)

    # def pprint(self, indent: int = 0, with_lines: bool = False):
    #     """
    #     Prints the OuDia file in a pretty format.

    #     Args:
    #         indent (int, optional): The indentation level. Defaults to 0.
    #     """
    #     # print(
    #     #     " " * indent + str(self.file_type)
    #     #     if not with_lines
    #     #     else "|" * (indent + 1) + str(self.file_type)
    #     # )
    #     for child in self.children:
    #         child.pprint(indent + 2)
    #     # if self.aftermath:
    #     #     print(" " * indent + self.aftermath)

    @property
    def children(self) -> list["Node | TypedNode"]:
        return self._children

    @staticmethod
    def from_node(node: Node) -> "OuDia":
        assert node.type == "Root"
        return OuDia(
            file_type=FileType.from_str(node.attributes.get_required("FileType")),
            file_type_app_comment=node.trailing_attributes.get("FileTypeAppComment"),
            _children=node.children,
        )

    def to_node(self) -> Node:
        return Node(
            type=None,
            attributes=Attributes(
                ("FileType", str(self.file_type)),
            ),
            trailing_attributes=Attributes(("FileTypeAppComment", self.file_type_app_comment)),
            children=Children(self.children),
        )
