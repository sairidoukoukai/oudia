from dataclasses import dataclass, field

from .node import Attributes, Children, Node, TypedNode


@dataclass
class Eki(TypedNode):
    """駅"""

    # region Attributes

    ekimei: str
    """駅名"""

    ekimei_jikoku_ryaku: str | None
    """駅名の時刻表ビュー用略称"""

    ekimei_dia_ryaku: str | None
    """駅名の運用一覧図ビュー用略称"""

    ekijikokukeisiki: str
    """駅時刻形式"""

    ekikibo: str
    """駅規模"""

    down_main: int | None
    """下りメイン"""

    up_main: int | None
    """上りメイン"""

    brunch_core_eki_index: int | None
    """分岐駅設定の基幹駅駅インデックス"""

    brunch_opposite: bool | None
    """分岐駅設定が反対方向の場合"""

    loop_origin_eki_index: int | None
    """環状線設定の起点駅インデックス"""

    loop_opposite: bool | None
    """環状線が反対向きに設定の有無"""

    jikokuhyou_track_display_kudari: bool | None
    """時刻表で下り番線表示設定"""

    jikokuhyou_track_display_nobori: bool | None
    """時刻表で上り番線表示設定"""

    next_eki_distance: int | None
    """次駅までの距離(秒)"""

    # endregion

    jikokuhyou_track_omit: bool | None
    """時刻表トラックの省略"""

    jikokuhyou_jikoku_display_kudari: str | None
    """時刻表時刻表示（下り）"""

    jikokuhyou_jikoku_display_nobori: str | None
    """時刻表時刻表示（上り）"""

    jikokuhyou_syubetsu_change_display_kudari: str | None
    """時刻表変更表示（下り）"""

    jikokuhyou_syubetsu_change_display_nobori: str | None
    """時刻表変更表示（上り）"""

    diagram_color_next_eki: int | None
    """次駅の色"""

    jikokuhyou_outer_display_kudari: str | None
    """時刻表外表示（下り）"""

    jikokuhyou_outer_display_nobori: str | None
    """時刻表外表示（上り）"""

    operation_table_display_jikoku: bool | None
    """運用表で時刻を表示するかどうか"""

    diagram_track_display: bool | None
    """運用表で番線を表示するかどうか"""

    _children: list["Node | TypedNode"] = field(default_factory=list)

    @property
    def children(self) -> list["Node | TypedNode"]:
        return self._children

    @classmethod
    def from_node(cls, node: Node) -> "Eki":
        return cls(
            ekimei=node.attributes.get_required("Ekimei"),
            ekimei_jikoku_ryaku=node.attributes.get("EkimeiJikokuRyaku"),
            ekimei_dia_ryaku=node.attributes.get("EkimeiDiaRyaku"),
            ekijikokukeisiki=node.attributes.get_required(key="Ekijikokukeisiki"),
            ekikibo=node.attributes.get_required("Ekikibo"),
            down_main=node.attributes.get_int("DownMain"),
            up_main=node.attributes.get_int("UpMain"),
            brunch_core_eki_index=node.attributes.get_int("BrunchCoreEkiIndex"),
            brunch_opposite=node.attributes.get_bool("BrunchOpposite"),
            loop_origin_eki_index=node.attributes.get_int("LoopOriginEkiIndex"),
            loop_opposite=node.attributes.get_bool("LoopOpposite"),
            jikokuhyou_track_display_kudari=node.attributes.get_bool("JikokuhyouTrackDisplayKudari"),
            jikokuhyou_track_display_nobori=node.attributes.get_bool("JikokuhyouTrackDisplayNobori"),
            diagram_track_display=node.attributes.get_bool("DiagramTrackDisplay"),
            next_eki_distance=node.attributes.get_int("NextEkiDistance"),
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
            operation_table_display_jikoku=node.trailing_attributes.get_bool("OperationTableDisplayJikoku"),
            _children=node.children,
        )

    def to_node(self) -> Node:
        return Node(
            type="Eki",
            attributes=Attributes(
                ("Ekimei", self.ekimei),
                ("EkimeiJikokuRyaku", self.ekimei_jikoku_ryaku),
                ("EkimeiDiaRyaku", self.ekimei_dia_ryaku),
                ("Ekijikokukeisiki", self.ekijikokukeisiki),
                ("Ekikibo", self.ekikibo),
                ("DownMain", self.down_main),
                ("UpMain", self.up_main),
                ("BrunchCoreEkiIndex", self.brunch_core_eki_index),
                ("BrunchOpposite", self.brunch_opposite),
                ("LoopOriginEkiIndex", self.loop_origin_eki_index),
                ("LoopOpposite", self.loop_opposite),
                ("JikokuhyouTrackDisplayKudari", self.jikokuhyou_track_display_kudari),
                ("JikokuhyouTrackDisplayNobori", self.jikokuhyou_track_display_nobori),
                ("DiagramTrackDisplay", self.diagram_track_display),
                ("NextEkiDistance", self.next_eki_distance),
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
                ("OperationTableDisplayJikoku", self.operation_table_display_jikoku),
            ),
        )
