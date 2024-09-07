import inspect
from oudia.nodes.ressya import Ressya
from oudia.parser import parse


def parse_ressya(text: str) -> Ressya:
    ressya_node = next(parse(text))
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