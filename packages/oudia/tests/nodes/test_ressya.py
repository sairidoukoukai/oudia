from oudia.nodes.ressya import Ressya
from oudia.parser import parse


def test_ressya():
    ressya_str = """
Ressya.
Houkou=Kudari
Syubetsu=1
Ressyabangou=5001
EkiJikoku=,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1;520$3,1;52240$0,1;525$0,1;528$0,1;53130$0,1;534/$2
Operation73B=3/514$/C34;G31,0/8$515/$0
Operation78A=5/$0
.
    """.strip()

    ressya_node = list(parse(ressya_str))[0]

    print(ressya_node)

    ressya = Ressya.from_node(ressya_node)
    print(ressya)

    assert ressya_str == str(ressya)
