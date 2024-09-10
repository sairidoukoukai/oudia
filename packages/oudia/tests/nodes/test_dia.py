from oudia.nodes.dia import Nobori
from oudia.nodes.node import EntryList, Node, NodeList
from oudia.nodes.ressya import Ressya


def test_nobori_empty():
    empty_nobori = Nobori(ressya_list=NodeList(Ressya, []))

    assert empty_nobori.to_node() == Node(
        "Nobori",
        entries=EntryList(NodeList(Ressya, [])),
    )

    assert str(EntryList(NodeList(Ressya, []))) == ""

    assert str(empty_nobori) == "Nobori.\n."
