import logging
import oudia
from oudia.nodes.eki import Eki
from oudia.nodes.node import EntryList, Node, NodeList
from oudia.nodes.ressyasyubetsu import Ressyasyubetsu
import pytest


def test_invalid(caplog):
    # Invalid file type
    with pytest.raises(ValueError) as e:
        oudia.loads("invalid")


def test_unsupported_software(caplog):
    caplog.set_level(logging.WARNING)
    oudia.loads("FileType=NotOuDia\nRosen.\n.\nDispProp.\n.\n")
    assert 'Unsupported software: "NotOuDia"' in caplog.text

    # # Unsupported software


EMPTY_ROSEN = oudia.Rosen(
    "メロンキング線",
    None,
    None,
    None,
    NodeList(Eki, []),
    NodeList(Ressyasyubetsu, []),
    NodeList(Node, []),
    None,
    None,
    None,
    None,
    None,
)


def test_node_conversion() -> None:
    untyped_rosen_node = oudia.Node(
        type="Rosen",
        entries=EntryList(
            ("Rosenmei", "メロンキング線"),
            (None, NodeList(Eki)),
            (None, NodeList(Ressyasyubetsu)),
            (None, NodeList(Node)),
        ),
    )
    typed_rosen_node = EMPTY_ROSEN

    assert untyped_rosen_node == typed_rosen_node.to_node()
    assert typed_rosen_node.from_node(untyped_rosen_node) == typed_rosen_node
    assert untyped_rosen_node == typed_rosen_node


EMPTY_DISP_PROP = oudia.DispProp(
    [],
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    [],
    [],
    None,
    None,
    [],
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
)


def test_pprint():
    dia = oudia.loads(
        f"FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nDispProp.\n.\nFileTypeAppComment=OuDia.Py 0.0.0\n"
    )
    print(f"{dia=}")
    print(f"{dia.to_node()=}")
    dia.pprint()


def test_dumps_empty():
    assert (
        oudia.dumps(
            oudia.OuDia(
                file_type=oudia.FileType("OuDia", "1.02"),
                rosen=EMPTY_ROSEN,
                disp_prop=EMPTY_DISP_PROP,
                window_placement=None,
            )
        )
        == "FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nDispProp.\n.\n"
    )


def test_exporter():
    assert (
        oudia.dumps(
            oudia.OuDia(
                file_type=oudia.FileType("OuDia", "1.02"),
                rosen=EMPTY_ROSEN,
                disp_prop=EMPTY_DISP_PROP,
                window_placement=None,
                file_type_app_comment="OuDia.Py 0.0.0",
            )
        )
        == "FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nDispProp.\n.\nFileTypeAppComment=OuDia.Py 0.0.0\n"
    )
