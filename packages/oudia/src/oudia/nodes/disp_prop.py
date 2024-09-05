from dataclasses import dataclass, field
from .node import EntryList, NodeList, Node, TypedNode


@dataclass
class DispProp(TypedNode):
    """表示プロパティ"""

    jikokuhyou_font: list[str]
    """時刻表フォント"""

    jikokuhyou_v_font: str | None
    """時刻表縦書きフォント"""

    dia_ekimei_font: str | None
    """ダイヤ駅名フォント"""

    dia_jikoku_font: str | None
    """ダイヤ時刻フォント"""

    dia_ressya_font: str | None
    """ダイヤ列車フォント"""

    operation_table_font: str | None
    """運用表フォント"""

    all_operation_table_jikoku_font: str | None
    """全運用表時刻フォント"""

    comment_font: str | None
    """コメントフォント"""

    dia_moji_color: str | None
    """ダイヤ文字色"""

    dia_back_color: list[str]
    """ダイヤ背景色"""

    dia_haikei_color: list[str]
    """ダイヤ背景色"""

    dia_ressya_color: str | None
    """ダイヤ列車色"""

    dia_jiku_color: str | None
    """ダイヤ軸色"""

    jikokuhyou_back_color: list[str]
    """時刻表背景色"""

    std_ope_time_lower_color: str | None
    """基準運転時分未満時背景色"""

    std_ope_time_higher_color: str | None
    """基準運転時分超過時背景色"""

    std_ope_time_undef_color: str | None
    """基準運転時分未定義時背景色"""

    std_ope_time_illegal_color: str | None
    """基準運転時分不適切時背景色"""

    operation_string_color: str | None
    """運用表文字色"""

    operation_grid_color: str | None
    """運用表グリッド色"""

    ekimei_length: int | None
    """駅名欄の幅"""

    jikokuhyou_ressya_width: int | None
    """時刻表列車欄の幅"""

    any_second_inc_dec1: int | None
    """任意秒移動1"""

    any_second_inc_dec2: int | None
    """任意秒移動2"""

    display_ressyamei: bool | None
    """列車名・号数の表示"""

    display_outer_terminal_ekimei_origin_side: bool | None
    """起点側の路線外発着欄表示"""

    display_outer_terminal_ekimei_terminal_side: bool | None
    """終点側の路線外発着欄表示"""

    diagram_display_outer_terminal: int | None
    """路線外発着欄表示方法"""

    second_round_chaku: int | None
    """着時刻秒処理方法"""

    second_round_hatsu: int | None
    """発時刻秒処理方法"""

    display_2400: bool | None
    """2400時刻表示"""

    operation_number_rows: int | None
    """運用番号欄の段数"""

    display_in_out_link_code: bool | None
    """入出区連携コード欄表示"""

    # TODO: Continue here
    ekimei_length: int | None

    @staticmethod
    def from_node(node: Node) -> "DispProp":
        return DispProp(
            jikokuhyou_font=node.entries.get_repeatable("JikokuhyouFont"),
            jikokuhyou_v_font=node.entries.get("JikokuhyouVFont"),
            dia_ekimei_font=node.entries.get("DiaEkimeiFont"),
            dia_jikoku_font=node.entries.get("DiaJikokuFont"),
            dia_ressya_font=node.entries.get("DiaRessyaFont"),
            operation_table_font=node.entries.get("OperationTableFont"),
            all_operation_table_jikoku_font=node.entries.get("AllOperationTableJikokuFont"),
            comment_font=node.entries.get("CommentFont"),
            dia_moji_color=node.entries.get("DiaMojiColor"),
            dia_back_color=node.entries.get_repeatable("DiaBackColor"),
            dia_haikei_color=node.entries.get_repeatable("DiaHaikeiColor"),
            dia_ressya_color=node.entries.get("DiaRessyaColor"),
            dia_jiku_color=node.entries.get("DiaJikuColor"),
            jikokuhyou_back_color=node.entries.get_repeatable("JikokuhyouBackColor"),
            std_ope_time_lower_color=node.entries.get("StdOpeTimeLowerColor"),
            std_ope_time_higher_color=node.entries.get("StdOpeTimeHigherColor"),
            std_ope_time_undef_color=node.entries.get("StdOpeTimeUndefColor"),
            std_ope_time_illegal_color=node.entries.get("StdOpeTimeIllegalColor"),
            operation_string_color=node.entries.get("OperationStringColor"),
            operation_grid_color=node.entries.get("OperationGridColor"),
            # TODO: Continue here
            ekimei_length=node.entries.get_int("EkimeiLength"),
            jikokuhyou_ressya_width=node.entries.get_int("JikokuhyouRessyaWidth"),
            any_second_inc_dec1=node.entries.get_int("AnySecondIncDec1"),
            any_second_inc_dec2=node.entries.get_int("AnySecondIncDec2"),
            display_ressyamei=node.entries.get_bool("DisplayRessyamei"),
            display_outer_terminal_ekimei_origin_side=node.entries.get_bool("DisplayOuterTerminalEkimeiOriginSide"),
            display_outer_terminal_ekimei_terminal_side=node.entries.get_bool("DisplayOuterTerminalEkimeiTerminalSide"),
            diagram_display_outer_terminal=node.entries.get_int("DiagramDisplayOuterTerminal"),
            second_round_chaku=node.entries.get_int("SecondRoundChaku"),
            second_round_hatsu=node.entries.get_int("SecondRoundHatsu"),
            display_2400=node.entries.get_bool("Display2400"),
            operation_number_rows=node.entries.get_int("OperationNumberRows"),
            display_in_out_link_code=node.entries.get_bool("DisplayInOutLinkCode"),
        )

    def to_node(self) -> Node:
        return Node(
            type="DispProp",
            entries=EntryList(
                *((f"JikokuhyouFont", v) for v in self.jikokuhyou_font),
                ("JikokuhyouVFont", self.jikokuhyou_v_font),
                ("DiaEkimeiFont", self.dia_ekimei_font),
                ("DiaJikokuFont", self.dia_jikoku_font),
                ("DiaRessyaFont", self.dia_ressya_font),
                ("OperationTableFont", self.operation_table_font),
                ("AllOperationTableJikokuFont", self.all_operation_table_jikoku_font),
                ("CommentFont", self.comment_font),
                ("DiaMojiColor", self.dia_moji_color),
                *((f"DiaBackColor", v) for v in self.dia_back_color),
                *((f"DiaHaikeiColor", v) for v in self.dia_haikei_color),
                ("DiaRessyaColor", self.dia_ressya_color),
                ("DiaJikuColor", self.dia_jiku_color),
                *((f"JikokuhyouBackColor", v) for v in self.jikokuhyou_back_color),
                ("StdOpeTimeLowerColor", self.std_ope_time_lower_color),
                ("StdOpeTimeHigherColor", self.std_ope_time_higher_color),
                ("StdOpeTimeUndefColor", self.std_ope_time_undef_color),
                ("StdOpeTimeIllegalColor", self.std_ope_time_illegal_color),
                ("OperationStringColor", self.operation_string_color),
                ("OperationGridColor", self.operation_grid_color),
                ("EkimeiLength", self.ekimei_length),
                ("JikokuhyouRessyaWidth", self.jikokuhyou_ressya_width),
                ("AnySecondIncDec1", self.any_second_inc_dec1),
                ("AnySecondIncDec2", self.any_second_inc_dec2),
                ("DisplayRessyamei", self.display_ressyamei),
                ("DisplayOuterTerminalEkimeiOriginSide", self.display_outer_terminal_ekimei_origin_side),
                ("DisplayOuterTerminalEkimeiTerminalSide", self.display_outer_terminal_ekimei_terminal_side),
                ("DiagramDisplayOuterTerminal", self.diagram_display_outer_terminal),
                ("SecondRoundChaku", self.second_round_chaku),
                ("SecondRoundHatsu", self.second_round_hatsu),
                ("Display2400", self.display_2400),
                ("OperationNumberRows", self.operation_number_rows),
                ("DisplayInOutLinkCode", self.display_in_out_link_code),
            ),
        )
