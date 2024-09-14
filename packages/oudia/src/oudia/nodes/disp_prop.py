"""表示プロパティを扱うためのモジュールです。"""

from dataclasses import dataclass, field
from typing import Self
from .node import EntryList, NodeList, Node, TypedNode


@dataclass(kw_only=True)
class FontProperty:
    """フォントプロパティ"""

    point_text_height: int
    """文字のポイント高さ（文字サイズ）"""

    facename: str
    """書体名"""

    bold: bool = False
    """太字の有無"""

    itaric: bool = False
    """斜体の有無（`italic`の誤字、原文ママ）"""

    def __str__(self) -> str:
        result = ""
        result += f"PointTextHeight={self.point_text_height}"
        result += f";Facename={self.facename}"
        if self.bold:
            result += ";Bold=1"
        if self.itaric:
            result += ";Itaric=1"
        return result

    @classmethod
    def from_str(cls, text: str) -> Self:
        """文字列からフォントプロパティを生成します。"""
        parts = text.split(";")
        pairs = list(map(lambda x: x.split("=", 1), parts))
        entries = {pair[0]: pair[1] for pair in pairs}
        return cls(
            point_text_height=int(entries["PointTextHeight"]),
            facename=entries["Facename"],
            bold=entries["Bold"] == "1" if "Bold" in entries else False,
            itaric=entries["Itaric"] == "1" if "Itaric" in entries else False,
        )


@dataclass(kw_only=True)
class DispProp(TypedNode):
    """表示プロパティ"""

    jikokuhyou_font: list[FontProperty]
    """時刻表フォント"""

    jikokuhyou_v_font: FontProperty | None
    """時刻表縦書きフォント"""

    dia_ekimei_font: FontProperty | None
    """ダイヤ駅名フォント"""

    dia_jikoku_font: FontProperty | None
    """ダイヤ時刻フォント"""

    dia_ressya_font: FontProperty | None
    """ダイヤ列車フォント"""

    operation_table_font: FontProperty | None
    """運用表フォント"""

    all_operation_table_jikoku_font: FontProperty | None
    """全運用表時刻フォント"""

    comment_font: FontProperty | None
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
        """ノードから表示プロパティを生成します。"""
        return DispProp(
            jikokuhyou_font=[FontProperty.from_str(f) for f in node.entries.get_repeatable("JikokuhyouFont")],
            jikokuhyou_v_font=FontProperty.from_str(f) if (f := node.entries.get("JikokuhyouVFont")) else None,
            dia_ekimei_font=FontProperty.from_str(f) if (f := node.entries.get("DiaEkimeiFont")) else None,
            dia_jikoku_font=FontProperty.from_str(f) if (f := node.entries.get("DiaJikokuFont")) else None,
            dia_ressya_font=FontProperty.from_str(f) if (f := node.entries.get("DiaRessyaFont")) else None,
            operation_table_font=FontProperty.from_str(f) if (f := node.entries.get("OperationTableFont")) else None,
            all_operation_table_jikoku_font=(
                FontProperty.from_str(f) if (f := node.entries.get("AllOperationTableJikokuFont")) else None
            ),
            comment_font=FontProperty.from_str(f) if (f := node.entries.get("CommentFont")) else None,
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
        """表示プロパティをノードに変換します。"""
        return Node(
            type="DispProp",
            entries=EntryList(
                *((f"JikokuhyouFont", str(v)) for v in filter(bool, self.jikokuhyou_font)),
                ("JikokuhyouVFont", str(self.jikokuhyou_v_font) if self.jikokuhyou_v_font is not None else None),
                ("DiaEkimeiFont", str(self.dia_ekimei_font) if self.dia_ekimei_font is not None else None),
                ("DiaJikokuFont", str(self.dia_jikoku_font) if self.dia_jikoku_font is not None else None),
                ("DiaRessyaFont", str(self.dia_ressya_font) if self.dia_ressya_font is not None else None),
                (
                    "OperationTableFont",
                    str(self.operation_table_font) if self.operation_table_font is not None else None,
                ),
                (
                    "AllOperationTableJikokuFont",
                    (
                        str(self.all_operation_table_jikoku_font)
                        if self.all_operation_table_jikoku_font is not None
                        else None
                    ),
                ),
                ("CommentFont", str(self.comment_font) if self.comment_font is not None else None),
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
