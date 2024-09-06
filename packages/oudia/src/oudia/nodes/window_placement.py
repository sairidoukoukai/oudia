from dataclasses import dataclass
from typing import Self
from .node import EntryList, Node, NodeList, TypedNode


@dataclass
class ChildWindow(TypedNode):
    """子ウィンドウ"""

    window_type: int | None
    """ウィンドウタイプ"""

    dia_index: int | None
    """ダイヤインデックス"""

    x_pos: int | None
    """X座標"""

    y_pos: int | None
    """Y座標"""

    x_size: int | None
    """Xサイズ"""

    y_size: int | None
    """Yサイズ"""

    @classmethod
    def from_node(cls, node: Node) -> Self:
        return cls(
            window_type=node.entries.get_int("WindowType"),
            dia_index=node.entries.get_int("DiaIndex"),
            x_pos=node.entries.get_int("XPos"),
            y_pos=node.entries.get_int("YPos"),
            x_size=node.entries.get_int("XSize"),
            y_size=node.entries.get_int("YSize"),
        )

    def to_node(self) -> Node:
        return Node(
            type=self.__class__.__name__,
            entries=EntryList(
                ("WindowType", self.window_type),
                ("DiaIndex", self.dia_index),
                ("XPos", self.x_pos),
                ("YPos", self.y_pos),
                ("XSize", self.x_size),
                ("YSize", self.y_size),
            ),
        )


@dataclass
class WindowPlacement(TypedNode):
    """ウィンドウ配置"""

    rosen_view_width: int | None = None
    """路線ビューの幅"""

    child_windows: NodeList[ChildWindow] | None = None

    @classmethod
    def from_node(cls, node: Node) -> Self:
        return cls(
            rosen_view_width=node.entries.get_int("RosenViewWidth"),
            child_windows=node.entries.get_list_by_type(ChildWindow),
        )

    def to_node(self) -> Node:
        return Node(
            type=self.__class__.__name__,
            entries=EntryList(
                ("RosenViewWidth", self.rosen_view_width),
                NodeList(ChildWindow, self.child_windows),
            ),
        )
