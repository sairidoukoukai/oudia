import logging
import oudia
from oudia.nodes.node import Attributes, Children
import pytest


def test_invalid(caplog):
    # Invalid file type
    with pytest.raises(ValueError) as e:
        oudia.loads("invalid")

    # Unsupported software
    oudia.loads("FileType=NotOuDia")
    caplog.set_level(logging.WARNING)
    assert 'Unsupported software: "NotOuDia"' in caplog.text


def test_node_conversion() -> None:
    untyped_rosen_node = oudia.Node(
        type="Rosen",
        attributes=Attributes(("Rosenmei", "メロンキング線")),
        children=Children(),
        trailing_attributes=Attributes(),
    )
    typed_rosen_node = oudia.Rosen("メロンキング線")

    assert untyped_rosen_node == typed_rosen_node.to_node()
    assert typed_rosen_node.from_node(untyped_rosen_node) == typed_rosen_node
    assert untyped_rosen_node == typed_rosen_node


def test_parser():
    assert oudia.loads("FileType=OuDia.1.02") == oudia.OuDia(
        file_type=oudia.FileType("OuDia", "1.02"),
    )
    assert oudia.loads(
        "FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n."
    ) == oudia.OuDia(
        file_type=oudia.FileType("OuDia", "1.02"),
        _children=[oudia.Rosen("メロンキング線")],
    )
    assert oudia.loads(
        f"FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nFileTypeAppComment=OuDia.Py 0.0.0"
    ) == oudia.OuDia(
        file_type=oudia.FileType("OuDia", "1.02"),
        file_type_app_comment="OuDia.Py 0.0.0",
        _children=[oudia.Rosen("メロンキング線")],
        # oudia.Node("Rosen", {"Rosenmei": "メロンキング線"})],
    )


def test_pprint():
    dia = oudia.loads(
        f"FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nFileTypeAppComment=OuDia.Py 0.0.0\n"
    )
    print(f"{dia=}")
    print(f"{dia.to_node()=}")
    dia.pprint()


def test_exporter():
    assert (
        oudia.dumps(
            oudia.OuDia(
                file_type=oudia.FileType("OuDia", "1.02"),
                _children=[oudia.Rosen("メロンキング線")],
            )
        )
        == "FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\n"
    )

    assert (
        oudia.dumps(
            oudia.OuDia(
                file_type=oudia.FileType("OuDia", "1.02"),
                file_type_app_comment="OuDia.Py 0.0.0",
                _children=[oudia.Rosen("メロンキング線")],
            )
        )
        == "FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nFileTypeAppComment=OuDia.Py 0.0.0\n"
    )


def test_authenity():
    with open("./tests/empty.oud2", "r", encoding="utf-8-sig") as f:
        text = f.read()
        dia = oudia.loads(text)
        print(dia)
        print(dia.pprint())
    with open("./tests/empty_dumped.oud2", "w", encoding="utf-8-sig") as f:
        f.write(oudia.dumps(dia))
    assert oudia.dumps(dia) == text
