# region FontProperty

import inspect

from oudia.nodes.disp_prop import DispProp, FontProperty
from oudia.parser import parse


def test_font_property_to_str():
    font_property = FontProperty(
        point_text_height=10,
        facename="メロンキング",
        bold=True,
        itaric=True,
    )
    assert str(font_property) == "PointTextHeight=10;Facename=メロンキング;Bold=1;Itaric=1"

    assert FontProperty.from_str("PointTextHeight=10;Facename=メロンキング") == FontProperty(
        point_text_height=10,
        facename="メロンキング",
        bold=False,
        itaric=False,
    )


# endregion


def test_disp_prop_eki_order_of_old_oudia():
    """OuDia.6以前はダイヤ列車情報の駅順を持つ。"""
    disp_prop_str = inspect.cleandoc(
        """
            DispProp.
            DiaMojiColor=00000000
            DiaRessyaColor=00000000
            DiaJikuColor=00C0C0C0
            EkimeiLength=9
            DiaRessyajouhouHyoujiEkiOrderKudari=0
            DiaRessyajouhouHyoujiEkiOrderNobori=1
            .
        """
    )
    node = parse(disp_prop_str)
    assert node is not None
    disp_prop = DispProp.from_node(node)

    assert disp_prop.dia_ressyajouhou_hyouji_eki_order_kudari == 0
    assert disp_prop.dia_ressyajouhou_hyouji_eki_order_nobori == 1
    assert str(disp_prop) == disp_prop_str
