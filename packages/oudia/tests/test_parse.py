"""Test parsing and node replacing"""

import oudia


from oudia.nodes.node import EntryList, Node, NodeList
from oudia.nodes.track import EkiTrack2, EkiTrack2Cont
from oudia.parser import parse, replace_node, replace_node_list, replace_nodes_in_entry_list


EMPTY_DISP_PROP = oudia.DispProp(
    jikokuhyou_font=[],
    jikokuhyou_v_font=None,
    dia_ekimei_font=None,
    dia_jikoku_font=None,
    dia_ressya_font=None,
    operation_table_font=None,
    all_operation_table_jikoku_font=None,
    comment_font=None,
    dia_moji_color=None,
    dia_back_color=[],
    dia_haikei_color=[],
    dia_ressya_color=None,
    dia_jiku_color=None,
    jikokuhyou_back_color=[],
    std_ope_time_lower_color=None,
    std_ope_time_higher_color=None,
    std_ope_time_undef_color=None,
    std_ope_time_illegal_color=None,
    operation_string_color=None,
    operation_grid_color=None,
    ekimei_length=None,
    jikokuhyou_ressya_width=None,
    any_second_inc_dec1=None,
    any_second_inc_dec2=None,
    display_ressyamei=None,
    display_outer_terminal_ekimei_origin_side=None,
    display_outer_terminal_ekimei_terminal_side=None,
    diagram_display_outer_terminal=None,
    second_round_chaku=None,
    second_round_hatsu=None,
    display_2400=None,
    operation_number_rows=None,
    display_in_out_link_code=None,
)

# region parsing


def test_parse_unknown():
    assert oudia.parser.parse(
        "\n".join(
            [
                "Unknown.",
                "SomeProperty=Value",
                ".",
            ]
        )
    ) == Node("Unknown", EntryList(("SomeProperty", "Value")))


def test_parse_repeatable():
    assert oudia.parser.parse(
        "\n".join(["HasRepeatable.", "RepeatingProperty=Value1", "RepeatingProperty=Value2", "."])
    ) == Node("HasRepeatable", EntryList(("RepeatingProperty", "Value1"), ("RepeatingProperty", "Value2")))


def test_parse_with_empty_lines():
    assert oudia.parser.parse(
        "\n".join(
            [
                "",
                "Node.",
                "",
                "SomeProperty=Value",
                "",
                ".",
            ]
        )
    ) == Node("Node", EntryList(("SomeProperty", "Value")))


# def test_parse_node_list():
#     assert list(
#         oudia.parser.parse(
#             "\n".join(
#                 [
#                     "Node.",
#                     "SomeProperty=Value",
#                     ".",
#                     "Node.",
#                     "SomeProperty=Value",
#                     ".",
#                 ]
#             )
#         )
#     ) == [
#         Node("Node", EntryList(("SomeProperty", "Value"))),
#         Node("Node", EntryList(("SomeProperty", "Value"))),
#     ]


# def test_parse_children():
#     assert list(
#         oudia.parser.parse(
#             "\n".join(
#                 [
#                     "NodeCont.",
#                     "SomeProperty=Value",
#                     "Node.",
#                     "SomeProperty=Value",
#                     ".",
#                     "Node.",
#                     "SomeProperty=Value",
#                     ".",
#                     ".",
#                 ]
#             )
#         )
#     ) == [
#         Node(
#             "NodeCont",
#             EntryList(
#                 ("SomeProperty", "Value"),
#                 NodeList(
#                     Node,
#                     [
#                         Node(
#                             "Node",
#                             EntryList(("SomeProperty", "Value")),
#                         ),
#                         Node(
#                             "Node",
#                             EntryList(("SomeProperty", "Value")),
#                         ),
#                     ],
#                 ),
#             ),
#         )
#     ]


def test_parse_multi_children():
    assert oudia.parser.parse(
        "\n".join(
            [
                "NodeCont.",
                "SomeProperty=Value",
                "NodeA.",
                "SomeProperty=Value",
                ".",
                "NodeA.",
                "SomeProperty=Value",
                ".",
                "NodeB.",
                "SomeProperty=Value",
                ".",
                "NodeB.",
                "SomeProperty=Value",
                ".",
                ".",
            ]
        )
    ) == Node(
        "NodeCont",
        EntryList(
            ("SomeProperty", "Value"),
            NodeList(
                Node,
                [
                    Node(
                        "NodeA",
                        EntryList(("SomeProperty", "Value")),
                    ),
                    Node(
                        "NodeA",
                        EntryList(("SomeProperty", "Value")),
                    ),
                ],
            ),
            NodeList(
                Node,
                [
                    Node(
                        "NodeB",
                        EntryList(("SomeProperty", "Value")),
                    ),
                    Node(
                        "NodeB",
                        EntryList(("SomeProperty", "Value")),
                    ),
                ],
            ),
        ),
    )


def test_parse_complex_nesting():
    assert oudia.parser.parse(
        "\n".join(
            [
                "GrandParent.",
                "Name=John Doe",
                "Uncle.",
                "Name=Jim Doe",
                ".",
                "Uncle.",
                "Name=Jimmy Doe",
                ".",
                "Aunt.",
                "Name=Jane Doe",
                ".",
                "Parent.",
                "Name=John Jr. Doe",
                "Sibling.",
                "Name=Jane Jr. Doe",
                ".",
                "Child.",
                "Name=Johnny Doe",
                ".",
                ".",
                ".",
            ]
        )
    ) == Node(
        "GrandParent",
        EntryList(
            ("Name", "John Doe"),
            NodeList(
                Node,
                [
                    Node(
                        "Uncle",
                        EntryList(("Name", "Jim Doe")),
                    ),
                    Node(
                        "Uncle",
                        EntryList(("Name", "Jimmy Doe")),
                    ),
                ],
            ),
            NodeList(
                Node,
                [
                    Node(
                        "Aunt",
                        EntryList(("Name", "Jane Doe")),
                    ),
                ],
            ),
            NodeList(
                Node,
                [
                    Node(
                        "Parent",
                        EntryList(
                            ("Name", "John Jr. Doe"),
                            NodeList(
                                Node,
                                [
                                    Node(
                                        "Sibling",
                                        EntryList(("Name", "Jane Jr. Doe")),
                                    ),
                                ],
                            ),
                            NodeList(
                                Node,
                                [
                                    Node(
                                        "Child",
                                        EntryList(("Name", "Johnny Doe")),
                                    ),
                                ],
                            ),
                        ),
                    ),
                ],
            ),
        ),
    )


def test_parse_even_more_complex_nesting():
    assert oudia.parser.parse(
        "\n".join(
            [
                "GrandParent.",
                "Name=John Doe",
                "Uncle.",
                "Name=Jim Doe",
                ".",
                "Uncle.",
                "Name=Jimmy Doe",
                ".",
                "Aunt.",
                "Name=Jane Doe",
                ".",
                "Parent.",
                "Name=John Jr. Doe",
                "Sibling.",
                "Name=Jane Jr. Doe",
                ".",
                "Sibling.",
                "Name=Jane Jr2. Doe",
                ".",
                "AdoptedSibling.",
                "Name=Jane Jr3. Doe",
                ".",
                "Child.",
                "Name=Johnny Doe",
                ".",
                ".",
                ".",
                ".",
            ]
        )
    ) == Node(
        "GrandParent",
        EntryList(
            ("Name", "John Doe"),
            NodeList(
                Node,
                [
                    Node(
                        "Uncle",
                        EntryList(("Name", "Jim Doe")),
                    ),
                    Node(
                        "Uncle",
                        EntryList(("Name", "Jimmy Doe")),
                    ),
                ],
            ),
            NodeList(
                Node,
                [
                    Node(
                        "Aunt",
                        EntryList(("Name", "Jane Doe")),
                    ),
                ],
            ),
            NodeList(
                Node,
                [
                    Node(
                        "Parent",
                        EntryList(
                            ("Name", "John Jr. Doe"),
                            NodeList(
                                Node,
                                [
                                    Node(
                                        "Sibling",
                                        EntryList(("Name", "Jane Jr. Doe")),
                                    ),
                                    Node(
                                        "Sibling",
                                        EntryList(("Name", "Jane Jr2. Doe")),
                                    ),
                                ],
                            ),
                            NodeList(
                                Node,
                                [
                                    Node(
                                        "AdoptedSibling",
                                        EntryList(("Name", "Jane Jr3. Doe")),
                                    ),
                                ],
                            ),
                            NodeList(
                                Node,
                                [
                                    Node(
                                        "Child",
                                        EntryList(("Name", "Johnny Doe")),
                                    ),
                                ],
                            ),
                        ),
                    ),
                ],
            ),
        ),
    )


# def test_parse_real_node():
#     assert list(oudia.parser.parse("EkiTrack2.\nTrackName=1番線\n.\nEkiTrack2.\nTrackName=2番線\n.\n.")) == [
#         Node("EkiTrack2", EntryList(("TrackName", "1番線"))),
#         Node("EkiTrack2", EntryList(("TrackName", "2番線"))),
#     ]


def test_parse_eki_track2_cont():

    assert oudia.parser.parse(
        "EkiTrack2Cont.\nEkiTrack2.\nTrackName=1番線\n.\nEkiTrack2.\nTrackName=2番線\n.\n."
    ) == Node(
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


def test_replace_unknown_node_type() -> None:
    assert replace_node(
        Node(
            type="Unknown",
            entries=EntryList(("TrackName", "1番線")),
        )
    ) == Node(
        type="Unknown",
        entries=EntryList(("TrackName", "1番線")),
    )


# endregion
