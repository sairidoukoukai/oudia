"""Test parsing and node replacing"""

import oudia


from oudia.nodes.node import EntryList, Node, NodeList
from oudia.nodes.track import EkiTrack2, EkiTrack2Cont
from oudia.parser import parse, replace_node, replace_node_list, replace_nodes_in_entry_list


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

# region parsing


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


# endregion

# region node-replacing


def test_replace_single_node():
    assert replace_node(
        Node(
            type="EkiTrack2",
            entries=EntryList(("TrackName", "1番線")),
        )
    ) == EkiTrack2(track_name="1番線")


def test_replace_node_list():
    assert replace_node_list(
        NodeList(
            Node,
            [
                Node(
                    type="EkiTrack2",
                    entries=EntryList(("TrackName", "1番線")),
                ),
                Node(
                    type="EkiTrack2",
                    entries=EntryList(("TrackName", "2番線")),
                ),
            ],
        )
    ) == NodeList(EkiTrack2, [EkiTrack2(track_name="1番線"), EkiTrack2(track_name="2番線")])


def test_replace_nodes_in_entry_list() -> None:
    assert replace_nodes_in_entry_list(
        EntryList(
            NodeList(
                Node,
                [
                    Node(
                        type="EkiTrack2",
                        entries=EntryList(("TrackName", "1番線")),
                    ),
                    Node(
                        type="EkiTrack2",
                        entries=EntryList(("TrackName", "2番線")),
                    ),
                ],
            )
        )
    ) == EntryList(NodeList(EkiTrack2, [EkiTrack2(track_name="1番線"), EkiTrack2(track_name="2番線")]))


def test_replace_nested_nodes() -> None:
    replaced_node = replace_node(
        Node(
            type="EkiTrack2Cont",
            entries=EntryList(
                NodeList(
                    Node,
                    [
                        Node(
                            type="EkiTrack2",
                            entries=EntryList(("TrackName", "1番線")),
                        )
                    ],
                )
            ),
        )
    )

    assert replaced_node == EkiTrack2Cont(tracks=[EkiTrack2(track_name="1番線")])


# endregion
