import inspect
from oudia.nodes.ressya import Ressya
from oudia.parser import parse
import pytest


def parse_ressya(text: str) -> Ressya:
    ressya_node = parse(text)
    assert ressya_node is not None
    return Ressya.from_node(ressya_node)


def test_ressya():
    RESSYAS = [
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=5001
            EkiJikoku=,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1;520$3,1;52240$0,1;525$0,1;528$0,1;53130$0,1;534/$2
            Operation73B=3/514$/C34;G31,0/8$515/$0
            Operation78A=5/$0
            .
        """,
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=303
            EkiJikoku=1;750$0,2$0,1;815/815$0,1;820/820$0
            Operation0B=5/$
            Operation3A=5/$0
            .
        """,
    ]

    for ressya_str in RESSYAS:
        ressya_str = inspect.cleandoc(ressya_str)
        ressya = parse_ressya(ressya_str)
        assert ressya_str == str(ressya)


def test_ressya_invalid():
    RESSYAS = [
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=303
            EkiJikoku=1;750$0,2$0,1;815/815$0,1;820/820$0
            Operation15B=5/$
            Operation3A=5/$0
            .
        """,
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=303
            EkiJikoku=1;750$0,2$0,1;815/815$0,1;820/820$0
            Operation3B=5/$
            Operation15A=5/$0
            .
        """,
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=303
            EkiJikoku=1;750$0,2$0,1;815/815$0,1;820/820$0
            Operation3B.0A=5/$0
            .
        """,
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=303
            EkiJikoku=1;750$0,2$0,1;815/815$0,1;820/820$0
            Operation3A.0B=5/$0
            .
        """,
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=303
            EkiJikoku=1;750$0,2$0,1;815/815$0,1;820/820$0
            Operation3A=5/$0
            Operation3A.15B=5/$0
            .
        """,
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=303
            EkiJikoku=1;750$0,2$0,1;815/815$0,1;820/820$0
            Operation3A=5/$0
            Operation3A.15A=5/$0
            .
        """,
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=303
            EkiJikoku=1;750$0,2$0,1;815/815$0,1;820/820$0
            Operation3B=5/$0
            Operation3B.15A=5/$0
            .
        """,
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=303
            EkiJikoku=1;750$0,2$0,1;815/815$0,1;820/820$0
            Operation3B=5/$0
            Operation3B.15B=5/$0
            .
        """,
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=303
            EkiJikoku=,,,,,
            Operation0B=5/$0
            .
        """,
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=303
            EkiJikoku=,,,,,
            Operation3A=5/$0
            .
        """,
    ]

    for ressya_str in RESSYAS:
        ressya_str = inspect.cleandoc(ressya_str)
        with pytest.raises((ValueError, IndexError)):
            ressya = parse_ressya(ressya_str)

def test_ressya_legacy_operation_number():
    ressya_str = inspect.cleandoc(
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=0
            Ressyabangou=924
            EkiJikoku=,,1;1010,1;1012/1013,1;1021/1021
            RessyaTrack=,,0,0,1
            Bikou=所定1024
            OperationNumber=A
            .
        """
    )
    ressya = parse_ressya(ressya_str)

    assert ressya.ressya_track == ",,0,0,1"
    assert ressya.operation_number == "A"
    assert str(ressya) == ressya_str


def test_ressya_empty():
    ressya_str = inspect.cleandoc(
        """
            Ressya.
            .
        """
    )
    ressya = parse_ressya(ressya_str)

    assert ressya.houkou is None
    assert ressya.eki_jikoku_list == []
    assert str(ressya) == ressya_str


def test_ressya_canceled():
    ressya_str = inspect.cleandoc(
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Ressyabangou=303
            EkiJikoku=1;750$0,2$0,1;815/815$0
            Bikou=運休
            Canceled=1
            .
        """
    )
    ressya = parse_ressya(ressya_str)

    assert ressya.canceled is True
    assert str(ressya) == ressya_str


def test_ressya_legacy_syubetsu_change():
    ressya_str = inspect.cleandoc(
        """
            Ressya.
            Houkou=Kudari
            Syubetsu=1
            Gousuu=3
            SyubetsuChange=1
            EkiJikoku=1;750$0,1;815/815$0
            .
        """
    )
    ressya = parse_ressya(ressya_str)

    assert ressya.syubetsu_change is True
    assert str(ressya) == ressya_str
