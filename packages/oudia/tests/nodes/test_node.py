import oudia
from oudia.nodes.eki import Eki
from oudia.nodes.node import EntryList, Node, NodeList
from oudia.nodes.ressyasyubetsu import Ressyasyubetsu
from oudia.nodes.track import EkiTrack2, EkiTrack2Cont


def test_parse_unknown():
    assert list(
        oudia.parser.parse(
            "\n".join(
                [
                    "Unknown.",
                    "SomeProperty=Value",
                    ".",
                ]
            )
        )
    ) == [Node("Unknown", EntryList(("SomeProperty", "Value")))]


def test_parse_repeatable():
    assert list(
        oudia.parser.parse("\n".join(["HasRepeatable.", "RepeatingProperty=Value1", "RepeatingProperty=Value2", "."]))
    ) == [Node("HasRepeatable", EntryList(("RepeatingProperty", "Value1"), ("RepeatingProperty", "Value2")))]


def test_parse_node_list():
    assert list(
        oudia.parser.parse(
            "\n".join(
                [
                    "Node.",
                    "SomeProperty=Value",
                    ".",
                    "Node.",
                    "SomeProperty=Value",
                    ".",
                ]
            )
        )
    ) == [
        Node("Node", EntryList(("SomeProperty", "Value"))),
        Node("Node", EntryList(("SomeProperty", "Value"))),
    ]


def test_parse_children():
    assert list(
        oudia.parser.parse(
            "\n".join(
                [
                    "NodeCont.",
                    "SomeProperty=Value",
                    "Node.",
                    "SomeProperty=Value",
                    ".",
                    "Node.",
                    "SomeProperty=Value",
                    ".",
                    ".",
                ]
            )
        )
    ) == [
        Node(
            "NodeCont",
            EntryList(
                ("SomeProperty", "Value"),
                NodeList(
                    Node,
                    [
                        Node(
                            "Node",
                            EntryList(("SomeProperty", "Value")),
                        ),
                        Node(
                            "Node",
                            EntryList(("SomeProperty", "Value")),
                        ),
                    ],
                ),
            ),
        )
    ]


def test_parse_eki_track2_cont():

    assert list(
        oudia.parser.parse("EkiTrack2Cont.\nEkiTrack2.\nTrackName=1番線\n.\nEkiTrack2.\nTrackName=2番線\n.\n.")
    ) == [
        Node(
            "EkiTrack2Cont",
            EntryList(
                NodeList(
                    Node,
                    [
                        Node("EkiTrack2", EntryList(("TrackName", "1番線"))),
                        Node("EkiTrack2", EntryList(("TrackName", "2番線"))),
                    ],
                ),
            ),
        )
    ]


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
            NodeList(Eki),
            NodeList(Ressyasyubetsu),
            NodeList(Node),
        ),
    )
    typed_rosen_node = EMPTY_ROSEN

    assert untyped_rosen_node == typed_rosen_node.to_node()
    assert typed_rosen_node.from_node(untyped_rosen_node) == typed_rosen_node
    assert untyped_rosen_node == typed_rosen_node


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
