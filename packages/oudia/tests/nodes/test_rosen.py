import inspect

from oudia.nodes.rosen import Rosen
from oudia.parser import parse


def parse_rosen(text: str) -> Rosen:
    rosen_node = parse(text)
    assert rosen_node is not None
    return Rosen.from_node(rosen_node)


def test_rosen_entry_order():
    rosen_str = inspect.cleandoc(
        """
            Rosen.
            Rosenmei=再履バス
            KitenJikoku=000
            DiagramDgrYZahyouKyoriDefault=60
            EnableOperation=1
            OperationCrossKitenJikoku=1
            KijunDiaIndex=0
            Comment=
            .
        """
    )
    rosen = parse_rosen(rosen_str)

    assert rosen.enable_operation == 1
    assert rosen.operation_cross_kiten_jikoku is True
    assert str(rosen) == rosen_str
