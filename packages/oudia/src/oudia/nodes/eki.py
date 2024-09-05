from dataclasses import dataclass, field

from .node import Attributes, Children, Node, TypedNode


@dataclass
class Eki(TypedNode):
    """駅"""

    ekimei: str
    """駅名"""

    ekijikokukeisiki: str
    """駅時刻形式"""

    ekikibo: str
    """駅規模"""

    down_main: int | None = None
    """下りメイン"""

    up_main: int | None = None
    """上りメイン"""

    jikokuhyou_track_omit: bool | None = None
    """時刻表トラックの省略"""

    jikokuhyou_jikoku_display_kudari: str | None = None
    """時刻表時刻表示（下り）"""

    jikokuhyou_jikoku_display_nobori: str | None = None
    """時刻表時刻表示（上り）"""

    jikokuhyou_syubetsu_change_display_kudari: str | None = None
    """時刻表変更表示（下り）"""

    jikokuhyou_syubetsu_change_display_nobori: str | None = None
    """時刻表変更表示（上り）"""

    diagram_color_next_eki: int | None = None
    """次駅の色"""

    jikokuhyou_outer_display_kudari: str | None = None
    """時刻表外表示（下り）"""

    jikokuhyou_outer_display_nobori: str | None = None
    """時刻表外表示（上り）"""

    _children: list["Node | TypedNode"] = field(default_factory=list)

    @property
    def children(self) -> list["Node | TypedNode"]:
        return self._children

    @staticmethod
    def from_node(node: Node) -> "Eki":
        return Eki(
            ekimei=node.attributes.get_required("Ekimei"),
            ekijikokukeisiki=node.attributes.get_required(key="Ekijikokukeisiki"),
            ekikibo=node.attributes.get_required("Ekikibo"),
            down_main=node.attributes.get_int("DownMain"),
            up_main=node.attributes.get_int("UpMain"),
            jikokuhyou_track_omit=node.trailing_attributes.get_bool("JikokuhyouTrackOmit"),
            jikokuhyou_jikoku_display_kudari=node.trailing_attributes.get("JikokuhyouJikokuDisplayKudari"),
            jikokuhyou_jikoku_display_nobori=node.trailing_attributes.get("JikokuhyouJikokuDisplayNobori"),
            jikokuhyou_syubetsu_change_display_kudari=node.trailing_attributes.get(
                "JikokuhyouSyubetsuChangeDisplayKudari"
            ),
            jikokuhyou_syubetsu_change_display_nobori=(
                node.trailing_attributes.get("JikokuhyouSyubetsuChangeDisplayNobori")
            ),
            diagram_color_next_eki=node.trailing_attributes.get_int("DiagramColorNextEki"),
            jikokuhyou_outer_display_kudari=node.trailing_attributes.get("JikokuhyouOuterDisplayKudari"),
            jikokuhyou_outer_display_nobori=node.trailing_attributes.get("JikokuhyouOuterDisplayNobori"),
            _children=node.children,
        )

    def to_node(self) -> Node:
        return Node(
            type="Eki",
            attributes=Attributes(
                ("Ekimei", self.ekimei),
                ("Ekijikokukeisiki", self.ekijikokukeisiki),
                ("Ekikibo", self.ekikibo),
                ("DownMain", self.down_main),
                ("UpMain", self.up_main),
            ),
            children=Children(self.children),
            trailing_attributes=Attributes(
                ("JikokuhyouTrackOmit", self.jikokuhyou_track_omit),
                ("JikokuhyouJikokuDisplayKudari", self.jikokuhyou_jikoku_display_kudari),
                ("JikokuhyouJikokuDisplayNobori", self.jikokuhyou_jikoku_display_nobori),
                ("JikokuhyouSyubetsuChangeDisplayKudari", self.jikokuhyou_syubetsu_change_display_kudari),
                ("JikokuhyouSyubetsuChangeDisplayNobori", self.jikokuhyou_syubetsu_change_display_nobori),
                ("DiagramColorNextEki", self.diagram_color_next_eki),
                ("JikokuhyouOuterDisplayKudari", self.jikokuhyou_outer_display_kudari),
                ("JikokuhyouOuterDisplayNobori", self.jikokuhyou_outer_display_nobori),
            ),
        )
