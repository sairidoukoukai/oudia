from dataclasses import dataclass, field

from oudia.nodes.disp_prop import DispProp
from oudia.nodes.rosen import Rosen

from .node import EntryList, NodeList, Node, TypedNode


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

    rosen: Rosen
    """路線"""

    disp_prop: DispProp
    """表示プロパティ"""

    window_placement: Node | None
    """ウィンドの配置"""

    file_type_app_comment: str | None = None
    """ファイル形式のアプリコメント"""

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

    @classmethod
    def from_node(cls, node: Node) -> "OuDia":
        assert node.type == "Root"
        return cls(
            file_type=FileType.from_str(node.entries.get_required("FileType")),
            rosen=node.entries.get_list(0, Rosen)[0],
            disp_prop=node.entries.get_list(1, DispProp)[0],
            window_placement=v[0] if (v := node.entries.get_list(2, Node)) else None,
            file_type_app_comment=node.entries.get("FileTypeAppComment"),
        )

    def to_node(self) -> Node:
        return Node(
            type=None,
            entries=EntryList(
                ("FileType", str(self.file_type)),
                (None, NodeList(Rosen, [self.rosen])),
                (None, NodeList(DispProp, [self.disp_prop])),
                (None, NodeList(Node, [self.window_placement] if self.window_placement else [])),
                ("FileTypeAppComment", self.file_type_app_comment),
            ),
        )
