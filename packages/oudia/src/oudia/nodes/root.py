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

    file_type_app_comment_after_file_type: bool = False
    """アプリコメントをファイル形式の直後に置くかどうか

    OuDia.2・OuDia.3ではファイル形式の直後、それ以外では末尾に置かれる。
    書き出しで元の位置を保つために、読み込んだ位置をそのまま覚えておく。
    """

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

        app_comment_index = next(
            (i for i, entry in enumerate(node.entries) if isinstance(entry, tuple) and entry[0] == "FileTypeAppComment"),
            None,
        )
        first_node_index = next((i for i, entry in enumerate(node.entries) if isinstance(entry, NodeList)), None)

        return cls(
            file_type=node.entries.get_required("FileType"),
            rosen=node.entries.get_list_by_type(Rosen)[0],
            disp_prop=node.entries.get_list_by_type(DispProp)[0],
            window_placement=v[0] if (v := node.entries.get_list_by_type(WindowPlacement)) else None,
            file_type_app_comment=node.entries.get("FileTypeAppComment"),
            file_type_app_comment_after_file_type=(
                app_comment_index is not None and first_node_index is not None and app_comment_index < first_node_index
            ),
        )

    def to_node(self) -> Node:
        """OuDiaファイルの根ノードをノードに変換します。"""
        return Node(
            type=None,
            entries=EntryList(
                ("FileType", str(self.file_type)),
                (
                    "FileTypeAppComment",
                    self.file_type_app_comment if self.file_type_app_comment_after_file_type else None,
                ),
                NodeList(Rosen, [self.rosen]),
                NodeList(DispProp, [self.disp_prop]),
                NodeList(WindowPlacement, [self.window_placement] if self.window_placement else []),
                (
                    "FileTypeAppComment",
                    None if self.file_type_app_comment_after_file_type else self.file_type_app_comment,
                ),
            ),
        )
