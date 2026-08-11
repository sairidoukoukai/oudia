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
