import inspect

from oudia.nodes.eki import Eki
from oudia.parser import parse


def parse_eki(text: str) -> Eki:
    eki_node = parse(text)
    assert eki_node is not None
    return Eki.from_node(eki_node)


def test_eki_operation_display_order():
    eki_str = inspect.cleandoc(
        """
            Eki.
            Ekimei=東岡崎
            Ekijikokukeisiki=Jikokukeisiki_Hatsuchaku
            Ekikibo=Ekikibo_Ippan
            JikokuhyouOperationOrigin=1
            JikokuhyouOperationTerminal=1
            JikokuhyouOperationOriginDownBeforeUpAfter=1
            JikokuhyouOperationOriginDownAfterUpBefore=1
            JikokuhyouOperationTerminalDownBeforeUpAfter=1
            JikokuhyouOperationTerminalDownAfterUpBefore=1
            .
        """
    )
    eki = parse_eki(eki_str)

    assert eki.jikokuhyou_operation_origin_down_before_up_after is True
    assert eki.jikokuhyou_operation_terminal_down_after_up_before is True
    assert str(eki) == eki_str


def test_eki_display_attributes_of_1_17():
    eki_str = inspect.cleandoc(
        """
            Eki.
            Ekimei=東岡崎
            Ekijikokukeisiki=Jikokukeisiki_Hatsuchaku
            Ekikibo=Ekikibo_Ippan
            DiagramTrackDisplay=1
            DiagramTrackOmit=0,0,1,0
            JikokuhyouOuterDisplayKudari=1,1
            JikokuhyouOuterDisplayNobori=1,1
            JikokuhyouPrevSyubetsuChangeDisplayKudari=0,4,0,0,1
            JikokuhyouPrevSyubetsuChangeDisplayNobori=0,4,1,0,2
            JikokuhyouNyuusenJikokuDisplayKudari=1
            JikokuhyouNyuusenJikokuDisplayNobori=1
            .
        """
    )
    eki = parse_eki(eki_str)

    assert eki.diagram_track_omit == "0,0,1,0"
    assert eki.jikokuhyou_prev_syubetsu_change_display_kudari == "0,4,0,0,1"
    assert eki.jikokuhyou_nyuusen_jikoku_display_nobori is True
    assert str(eki) == eki_str
