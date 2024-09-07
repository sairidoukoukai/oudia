import oudia
from oudia.nodes.dia import Dia
from oudia.nodes.eki import Eki
from oudia.nodes.node import EntryList, Node, NodeList
from oudia.nodes.ressyasyubetsu import Ressyasyubetsu
from oudia.nodes.track import EkiTrack2, EkiTrack2Cont
import pytest


EMPTY_ROSEN = oudia.Rosen(
    rosenmei="メロンキング線",
    kudari_dia_alias=None,
    nobori_dia_alias=None,
    kiten_jikoku=None,
    enable_operation=None,
    eki_list=NodeList(Eki, []),
    ressyasyubetsu_list=NodeList(Ressyasyubetsu, []),
    dia_list=NodeList(Dia, []),
)

# region pprint


def test_node_pprint(capfd):
    dia = oudia.loads(
        f"FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nDispProp.\n.\nFileTypeAppComment=OuDia.Py 0.0.0\n"
    )
    dia.pprint()
    out, err = capfd.readouterr()
    assert (
        "  FileType=OuDia.1.02\n  Rosen.\n    Rosenmei=メロンキング線\n  .\n  DispProp.\n  .\n  FileTypeAppComment=OuDia.Py 0.0.0\n"
        in out
    )


def test_typed_node_pprint(capfd):
    dia = oudia.loads(
        f"FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nDispProp.\n.\nFileTypeAppComment=OuDia.Py 0.0.0\n"
    )
    dia.rosen.pprint()
    out, err = capfd.readouterr()
    assert "Rosen.\n  Rosenmei=メロンキング線\n." in out


def test_node_repr():
    assert (
        repr(
            Node(
                type="Rosen",
                entries=EntryList(
                    ("Rosenmei", "メロンキング線"),
                    NodeList(Eki),
                    NodeList(Ressyasyubetsu),
                    NodeList(Node),
                ),
            )
        )
        == "Node(type='Rosen', entries=EntryList(('Rosenmei', 'メロンキング線'), NodeList(Eki, []), NodeList(Ressyasyubetsu, []), NodeList(Node, [])))"
    )


# endregion

# region EntryList


def test_entry_list_get_required():
    assert EntryList(("Rosenmei", "メロンキング線")).get_required("Rosenmei") == "メロンキング線"

    with pytest.raises(expected_exception=ValueError):
        EntryList(("Rosenmei", "メロンキング線")).get_required("Rosenmei2")


def test_entry_parse_value():
    assert EntryList.parse_value(None) == ""


# endregion

# region conversion


def test_node_conversion() -> None:
    untyped_rosen_node = oudia.Node(
        type="Rosen",
        entries=EntryList(
            ("Rosenmei", "メロンキング線"),
            NodeList(Eki),
            NodeList(Ressyasyubetsu),
            NodeList(Node),
        ),
    )
    typed_rosen_node = EMPTY_ROSEN

    assert untyped_rosen_node == typed_rosen_node.to_node()
    assert typed_rosen_node.from_node(untyped_rosen_node) == typed_rosen_node
    assert untyped_rosen_node == typed_rosen_node


def test_node_equality() -> None:
    assert 0 != oudia.Node(
        type="Rosen",
        entries=EntryList(
            ("Rosenmei", "メロンキング線"),
            NodeList(Eki),
            NodeList(Ressyasyubetsu),
            NodeList(Node),
        ),
    )


# endregion


# region export
def test_export_ekitrack2cont():
    assert (
        str(
            EkiTrack2Cont(
                [
                    EkiTrack2(
                        track_name="1番線",
                    ),
                    EkiTrack2(
                        track_name="2番線",
                    ),
                ]
            )
        )
        == "EkiTrack2Cont.\nEkiTrack2.\nTrackName=1番線\n.\nEkiTrack2.\nTrackName=2番線\n.\n."
    )


def test_export_node_list():
    assert (
        str(
            NodeList(
                EkiTrack2,
                [
                    EkiTrack2(
                        track_name="1番線",
                    ),
                    EkiTrack2(
                        track_name="2番線",
                    ),
                ],
            )
        )
        == "EkiTrack2.\nTrackName=1番線\n.\nEkiTrack2.\nTrackName=2番線\n."
    )


# endregion
