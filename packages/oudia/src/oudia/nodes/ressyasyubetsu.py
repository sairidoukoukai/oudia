from dataclasses import dataclass, field

from .node import Attributes, Children, Node, TypedNode


@dataclass
class Ressyasyubetsu(TypedNode):
    """列車種別"""

    syubetsumei: str
    """種別名"""

    ryakusyo: str | None
    """略称"""

    jikokuhyou_moji_color: str
    """時刻表文字カラー"""

    jikokuhyou_font_index: str
    """時刻表文字フォントインデックス"""

    jikokuhyou_back_color: str
    """時刻表文字背景カラー"""

    diagram_sen_color: str
    """ダイヤグラム線カラー"""

    diagram_sen_style: str
    """ダイヤグラム線スタイル"""

    diagram_sen_is_bold: bool | None
    """ダイヤグラム太線"""

    stop_mark_draw_type: str | None
    """停止マーク描画タイプ"""

    parent_syubetsu_index: int | None
    """親種別インデックス"""

    _children: list["Node | TypedNode"] = field(default_factory=list)

    @property
    def children(self) -> list["Node | TypedNode"]:
        return self._children

    @staticmethod
    def from_node(node: Node) -> "Ressyasyubetsu":
        return Ressyasyubetsu(
            syubetsumei=node.attributes.get_required("Syubetsumei"),
            ryakusyo=node.attributes.get("Ryakusyo"),
            jikokuhyou_moji_color=node.attributes.get_required("JikokuhyouMojiColor"),
            jikokuhyou_font_index=node.attributes.get_required("JikokuhyouFontIndex"),
            jikokuhyou_back_color=node.attributes.get_required("JikokuhyouBackColor"),
            diagram_sen_color=node.attributes.get_required("DiagramSenColor"),
            diagram_sen_style=node.attributes.get_required("DiagramSenStyle"),
            diagram_sen_is_bold=node.attributes.get("DiagramSenIsBold") == "1",
            stop_mark_draw_type=node.attributes.get_required("StopMarkDrawType"),
            parent_syubetsu_index=(
                int(v)
                if (v := node.trailing_attributes.get("ParentSyubetsuIndex"))
                else None
            ),
            _children=node.children,
        )

    def to_node(self) -> Node:
        return Node(
            type="Ressyasyubetsu",
            attributes=Attributes(
                ("Syubetsumei", self.syubetsumei),
                ("Ryakusyo", self.ryakusyo),
                ("JikokuhyouMojiColor", self.jikokuhyou_moji_color),
                ("JikokuhyouFontIndex", self.jikokuhyou_font_index),
                ("JikokuhyouBackColor", self.jikokuhyou_back_color),
                ("DiagramSenColor", self.diagram_sen_color),
                ("DiagramSenStyle", self.diagram_sen_style),
                ("DiagramSenIsBold", "1" if self.diagram_sen_is_bold else "0"),
                ("StopMarkDrawType", self.stop_mark_draw_type),
                (
                    "ParentSyubetsuIndex",
                    (
                        str(self.parent_syubetsu_index)
                        if self.parent_syubetsu_index
                        else None
                    ),
                ),
            ),
            children=Children(),
            trailing_attributes=Attributes(),
        )
