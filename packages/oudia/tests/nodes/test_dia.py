import inspect

from oudia.nodes.dia import Dia, Nobori
from oudia.nodes.node import EntryList, Node, NodeList
from oudia.nodes.ressya import Ressya
from oudia.parser import parse


def parse_dia(text: str) -> Dia:
    dia_node = parse(text)
    assert dia_node is not None
    return Dia.from_node(dia_node)


def test_nobori_empty():
    empty_nobori = Nobori(ressya_list=NodeList(Ressya, []))

    assert empty_nobori.to_node() == Node(
        "Nobori",
        entries=EntryList(NodeList(Ressya, [])),
    )

    assert str(EntryList(NodeList(Ressya, []))) == ""

    assert str(empty_nobori) == "Nobori.\n."


def test_dia_pattern_diagram_preview():
    dia_str = inspect.cleandoc(
        """
            Dia.
            DiaName=平日
            MainBackColorIndex=0
            SubBackColorIndex=1
            BackPatternIndex=0
            PatternDiagramPreviewEnable=1
            PatternDiagramPreviewCycleSecond=600
            .
        """
    )
    dia = parse_dia(dia_str)

    assert dia.pattern_diagram_preview_enable is True
    assert dia.pattern_diagram_preview_cycle_second == 600
    assert str(dia) == dia_str
