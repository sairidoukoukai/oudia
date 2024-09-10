# region FontProperty


from oudia.nodes.disp_prop import FontProperty


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
