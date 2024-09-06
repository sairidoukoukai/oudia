import oudia
from oudia.nodes.node import EntryList, Node, NodeList
from oudia.nodes.track import EkiTrack2, EkiTrack2Cont


def test_parse_unknown():
    assert list(
        oudia.parser.parse(
            [
                "Unknown.",
                "SomeProperty=Value",
                ".",
            ]
        )
    ) == [Node("Unknown", EntryList(("SomeProperty", "Value")))]


def test_parse_repeatable():
    assert list(
        oudia.parser.parse(["HasRepeatable.", "RepeatingProperty=Value1", "RepeatingProperty=Value2", "."])
    ) == [Node("HasRepeatable", EntryList(("RepeatingProperty", "Value1"), ("RepeatingProperty", "Value2")))]


def test_parse_node_list():
    assert list(
        oudia.parser.parse(
            [
                "Node.",
                "SomeProperty=Value",
                ".",
                "Node.",
                "SomeProperty=Value",
                ".",
            ]
        )
    ) == [
        Node("Node", EntryList(("SomeProperty", "Value"))),
        Node("Node", EntryList(("SomeProperty", "Value"))),
    ]


def test_parse_children():
    assert list(
        oudia.parser.parse(
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
        oudia.parser.parse(
            "EkiTrack2Cont.\nEkiTrack2.\nTrackName=1番線\n.\nEkiTrack2.\nTrackName=2番線\n.\n.".splitlines()
        )
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