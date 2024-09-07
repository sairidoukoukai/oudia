from oudia.nodes.node import EntryList, Node, NodeList
from oudia.nodes.track import EkiTrack2, EkiTrack2Cont


def test_eki_track_2_from_node():
    assert EkiTrack2.from_node(Node(type="EkiTrack2", entries=EntryList(("TrackName", "1番線")))) == EkiTrack2(
        track_name="1番線"
    )


def test_eki_track_2_to_node():
    assert EkiTrack2(track_name="1番線").to_node() == Node(
        type="EkiTrack2",
        entries=EntryList(("TrackName", "1番線")),
    )


def test_eki_track_2_cont_from_node():
    assert EkiTrack2Cont.from_node(
        Node(type="EkiTrack2Cont", entries=EntryList(NodeList(EkiTrack2, [EkiTrack2(track_name="1番線")])))
    ) == EkiTrack2Cont(tracks=[EkiTrack2(track_name="1番線")])


def test_eki_track_2_cont_to_node():
    assert EkiTrack2Cont(tracks=[EkiTrack2(track_name="1番線")]).to_node() == Node(
        type="EkiTrack2Cont",
        entries=EntryList(NodeList(EkiTrack2, [EkiTrack2(track_name="1番線")])),
    )
