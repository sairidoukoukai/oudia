import inspect

from oudia.nodes.ressyasyubetsu import Ressyasyubetsu
from oudia.parser import parse


def parse_ressyasyubetsu(text: str) -> Ressyasyubetsu:
    node = parse(text)
    assert node is not None
    return Ressyasyubetsu.from_node(node)


def test_ressyasyubetsu_hidden():
    syubetsu_str = inspect.cleandoc(
        """
            Ressyasyubetsu.
            Syubetsumei=普通
            Ryakusyou=普
            JikokuhyouMojiColor=00000000
            DiagramSenColor=00000000
            DiagramSenStyle=SenStyle_Jissen
            StopMarkDrawType=EStopMarkDrawType_DrawOnStop
            ParentSyubetsuIndex=0
            Hidden=1
            .
        """
    )
    syubetsu = parse_ressyasyubetsu(syubetsu_str)

    assert syubetsu.hidden is True
    assert str(syubetsu) == syubetsu_str


def test_ressyasyubetsu_diagram_ressya_font():
    syubetsu_str = inspect.cleandoc(
        """
            Ressyasyubetsu.
            Syubetsumei=普通
            Ryakusyou=普
            JikokuhyouMojiColor=00000000
            DiagramSenColor=00000000
            DiagramSenStyle=SenStyle_Jissen
            DiagramRessyaFont=PointTextHeight=9;Facename=ＭＳ ゴシック
            StopMarkDrawType=EStopMarkDrawType_DrawOnStop
            .
        """
    )
    syubetsu = parse_ressyasyubetsu(syubetsu_str)

    assert syubetsu.diagram_ressya_font == "PointTextHeight=9;Facename=ＭＳ ゴシック"
    assert str(syubetsu) == syubetsu_str
