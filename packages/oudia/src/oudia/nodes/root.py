"""OuDiaファイル全体を扱うためのモジュールです。"""

from dataclasses import dataclass, field

from oudia.nodes.disp_prop import DispProp
from oudia.nodes.rosen import Rosen
from oudia.nodes.window_placement import WindowPlacement

from .node import EntryList, NodeList, Node, TypedNode


@dataclass(kw_only=True)
class OuDia(TypedNode):
    """OuDiaファイル"""

    file_type: str
    """ファイル形式"""

    rosen: Rosen
    """路線"""

    disp_prop: DispProp
    """表示プロパティ"""

    window_placement: WindowPlacement | None
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
        """ノードからOuDiaファイルの根ノードを生成します。"""
        assert node.type == "Root"
        return cls(
            file_type=node.entries.get_required("FileType"),
            rosen=node.entries.get_list_by_type(Rosen)[0],
            disp_prop=node.entries.get_list_by_type(DispProp)[0],
            window_placement=v[0] if (v := node.entries.get_list_by_type(WindowPlacement)) else None,
            file_type_app_comment=node.entries.get("FileTypeAppComment"),
        )

    def to_node(self) -> Node:
        """OuDiaファイルの根ノードをノードに変換します。"""
        return Node(
            type=None,
            entries=EntryList(
                ("FileType", str(self.file_type)),
                NodeList(Rosen, [self.rosen]),
                NodeList(DispProp, [self.disp_prop]),
                NodeList(WindowPlacement, [self.window_placement] if self.window_placement else []),
                ("FileTypeAppComment", self.file_type_app_comment),
            ),
        )
