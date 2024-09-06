import oudia
from oudia.nodes import EkiTrack2Cont, EkiTrack2
from oudia.nodes.node import NodeList


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
