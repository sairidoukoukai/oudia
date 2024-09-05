from dataclasses import dataclass, field

from .node import EntryList, NodeList, Node, TypedNode


@dataclass
class Ressyasyubetsu(TypedNode):
    """列車種別"""

    syubetsumei: str
    """種別名"""

    ryakusyou: str | None
    """略称"""

    jikokuhyou_moji_color: str
    """時刻表文字色"""

    jikokuhyou_font_index: str
    """時刻表文字フォントインデックス"""

    jikokuhyou_back_color: str
    """時刻表文字背景色"""

    diagram_sen_color: str
    """ダイヤグラム線色"""

    diagram_sen_style: str
    """ダイヤグラム線スタイル"""

    diagram_sen_is_bold: bool | None
    """ダイヤグラム太線"""

    stop_mark_draw_type: str | None
    """停止マーク描画タイプ"""

    parent_syubetsu_index: int | None
    """親種別インデックス"""

    @classmethod
    def from_node(cls, node: Node) -> "Ressyasyubetsu":
        return cls(
            syubetsumei=node.entries.get_required("Syubetsumei"),
            ryakusyou=node.entries.get("Ryakusyou"),
            jikokuhyou_moji_color=node.entries.get_required("JikokuhyouMojiColor"),
            jikokuhyou_font_index=node.entries.get_required("JikokuhyouFontIndex"),
            jikokuhyou_back_color=node.entries.get_required("JikokuhyouBackColor"),
            diagram_sen_color=node.entries.get_required("DiagramSenColor"),
            diagram_sen_style=node.entries.get_required("DiagramSenStyle"),
            diagram_sen_is_bold=node.entries.get_bool("DiagramSenIsBold"),
            stop_mark_draw_type=node.entries.get_required("StopMarkDrawType"),
            parent_syubetsu_index=node.entries.get_int("ParentSyubetsuIndex"),
        )

    def to_node(self) -> Node:
        return Node(
            type="Ressyasyubetsu",
            entries=EntryList(
                ("Syubetsumei", self.syubetsumei),
                ("Ryakusyou", self.ryakusyou),
                ("JikokuhyouMojiColor", self.jikokuhyou_moji_color),
                ("JikokuhyouFontIndex", self.jikokuhyou_font_index),
                ("JikokuhyouBackColor", self.jikokuhyou_back_color),
                ("DiagramSenColor", self.diagram_sen_color),
                ("DiagramSenStyle", self.diagram_sen_style),
                ("DiagramSenIsBold", self.diagram_sen_is_bold),
                ("StopMarkDrawType", self.stop_mark_draw_type),
                ("ParentSyubetsuIndex", self.parent_syubetsu_index),
            ),
        )
