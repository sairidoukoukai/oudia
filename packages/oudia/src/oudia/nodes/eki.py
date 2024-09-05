from dataclasses import dataclass, field

from oudia.nodes.track import EkiTrack2

from .node import EntryList, NodeList, Node, TypedNode


@dataclass
class Eki(TypedNode):
    """駅"""

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

    diagram_ressyajouhou_hyouji_kudari: str
    """ダイヤ列車情報表示形式（下り）"""

    diagram_ressyajouhou_hyouji_nobori: str
    """ダイヤ列車情報表示形式（上り）"""

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

    diagram_track_display: bool | None
    """ダイヤ列車で番線表示設定"""

    eki_tracks: NodeList[EkiTrack2]
    """駅の番線"""

    outer_terminal: NodeList[Node]
    """時刻表外表示の端末名"""

    next_eki_distance: int | None
    """次駅までの距離(秒)"""

    jikokuhyou_track_omit: bool | None
    """時刻表トラックの省略"""

    jikokuhyou_operation_origin: int | None
    """起点側作業表示欄の数"""

    jikokuhyou_operation_terminal: int | None
    """終点側作業表示欄の数"""

    jikokuhyou_operation_origin_down_before_up_after: bool | None
    """起点側作業表示欄（下り）（前後）"""

    jikokuhyou_operation_origin_down_after_up_before: bool | None
    """起点側作業表示欄（上り）（前後）"""

    jikokuhyou_operation_terminal_down_before_up_after: bool | None
    """終点側作業表示欄（下り）（前後）"""

    jikokuhyou_operation_terminal_down_after_up_before: bool | None
    """終点側作業表示欄（上り）（前後）"""

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

    crossing_check_rule_list: NodeList[Node] | None
    """クローシング通過チェックルールリスト"""

    diagram_track_display: bool | None
    """運用表で番線を表示するかどうか"""

    _children: list["Node | TypedNode"] = field(default_factory=list)

    @property
    def children(self) -> list["Node | TypedNode"]:
        return self._children

    @classmethod
    def from_node(cls, node: Node) -> "Eki":
        return cls(
            ekimei=node.entries.get_required("Ekimei"),
            ekimei_jikoku_ryaku=node.entries.get("EkimeiJikokuRyaku"),
            ekimei_dia_ryaku=node.entries.get("EkimeiDiaRyaku"),
            ekijikokukeisiki=node.entries.get_required(key="Ekijikokukeisiki"),
            ekikibo=node.entries.get_required("Ekikibo"),
            diagram_ressyajouhou_hyouji_kudari=node.entries.get_bool("DiagramRessyajouhouHyoujiKudari"),
            diagram_ressyajouhou_hyouji_nobori=node.entries.get_bool("DiagramRessyajouhouHyoujiNobori"),
            diagram_color_next_eki=node.entries.get_int("DiagramColorNextEki"),
            diagram_track_display=node.entries.get_bool("DiagramTrackDisplay"),
            outer_terminal=node.entries.get_list(0, Node),
            jikokuhyou_operation_origin=node.entries.get_list(1, Node),
            jikokuhyou_operation_terminal=node.entries.get_list(2, Node),
            jikokuhyou_operation_origin_down_before_up_after=node.entries.get_bool(
                "JikokuhyouOperationOriginDownBeforeUpAfter"
            ),
            jikokuhyou_operation_origin_down_after_up_before=node.entries.get_bool(
                "JikokuhyouOperationOriginDownAfterUpBefore"
            ),
            jikokuhyou_operation_terminal_down_before_up_after=node.entries.get_bool(
                "JikokuhyouOperationTerminalDownBeforeUpAfter"
            ),
            jikokuhyou_operation_terminal_down_after_up_before=node.entries.get_bool(
                "JikokuhyouOperationTerminalDownAfterUpBefore"
            ),
            down_main=node.entries.get_int("DownMain"),
            up_main=node.entries.get_int("UpMain"),
            brunch_core_eki_index=node.entries.get_int("BrunchCoreEkiIndex"),
            brunch_opposite=node.entries.get_bool("BrunchOpposite"),
            loop_origin_eki_index=node.entries.get_int("LoopOriginEkiIndex"),
            loop_opposite=node.entries.get_bool("LoopOpposite"),
            jikokuhyou_track_display_kudari=node.entries.get_bool("JikokuhyouTrackDisplayKudari"),
            jikokuhyou_track_display_nobori=node.entries.get_bool("JikokuhyouTrackDisplayNobori"),
            next_eki_distance=node.entries.get_int("NextEkiDistance"),
            eki_tracks=node.entries.get_list(3, EkiTrack2),
            jikokuhyou_track_omit=node.entries.get_bool("JikokuhyouTrackOmit"),
            jikokuhyou_jikoku_display_kudari=node.entries.get("JikokuhyouJikokuDisplayKudari"),
            jikokuhyou_jikoku_display_nobori=node.entries.get("JikokuhyouJikokuDisplayNobori"),
            jikokuhyou_syubetsu_change_display_kudari=node.entries.get("JikokuhyouSyubetsuChangeDisplayKudari"),
            jikokuhyou_syubetsu_change_display_nobori=(node.entries.get("JikokuhyouSyubetsuChangeDisplayNobori")),
            jikokuhyou_outer_display_kudari=node.entries.get("JikokuhyouOuterDisplayKudari"),
            jikokuhyou_outer_display_nobori=node.entries.get("JikokuhyouOuterDisplayNobori"),
            crossing_check_rule_list=node.entries.get_list(4, Node),
            operation_table_display_jikoku=node.entries.get_bool("OperationTableDisplayJikoku"),
        )

    # Arguments missing for parameters "diagram_ressyajouhou_hyouji_kudari", "diagram_ressyajouhou_hyouji_nobori", "outer_terminal", "jikokuhyou_operation_origin", "jikokuhyou_operation_terminal", "jikokuhyou_operation_origin_down_before_up_after", "jikokuhyou_operation_origin_down_after_up_before", "jikokuhyou_operation_terminal_down_before_up_after", "jikokuhyou_operation_terminal_down_after_up_before"PylancereportCallIssue
    # Codeium: Explain Problem

    def to_node(self) -> Node:
        return Node(
            type="Eki",
            entries=EntryList(
                ("Ekimei", self.ekimei),
                ("EkimeiJikokuRyaku", self.ekimei_jikoku_ryaku),
                ("EkimeiDiaRyaku", self.ekimei_dia_ryaku),
                ("Ekijikokukeisiki", self.ekijikokukeisiki),
                ("Ekikibo", self.ekikibo),
                ("DiagramRessyajouhouHyoujiKudari", self.diagram_ressyajouhou_hyouji_kudari),
                ("DiagramRessyajouhouHyoujiNobori", self.diagram_ressyajouhou_hyouji_nobori),
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
                (None, self.eki_tracks),
                ("JikokuhyouTrackOmit", self.jikokuhyou_track_omit),
                ("JikokuhyouJikokuDisplayKudari", self.jikokuhyou_jikoku_display_kudari),
                ("JikokuhyouJikokuDisplayNobori", self.jikokuhyou_jikoku_display_nobori),
                ("DiagramTrackDisplay", self.diagram_track_display),
                (None, self.eki_tracks),
                ("JikokuhyouSyubetsuChangeDisplayKudari", self.jikokuhyou_syubetsu_change_display_kudari),
                ("JikokuhyouSyubetsuChangeDisplayNobori", self.jikokuhyou_syubetsu_change_display_nobori),
                ("DiagramColorNextEki", self.diagram_color_next_eki),
                ("JikokuhyouOuterDisplayKudari", self.jikokuhyou_outer_display_kudari),
                ("JikokuhyouOuterDisplayNobori", self.jikokuhyou_outer_display_nobori),
                ("OperationTableDisplayJikoku", self.operation_table_display_jikoku),
                (None, self.crossing_check_rule_list),
            ),
        )
