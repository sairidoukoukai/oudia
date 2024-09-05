from dataclasses import dataclass, field
from typing import Sequence
from .node import EntryList, NodeList, Node, TypedNode


@dataclass
class EkiTrack2(TypedNode):
    """駅トラック2"""

    track_name: str
    """トラック名"""

    track_ryakusyo: str | None
    """トラック略称"""

    track_nobori_ryakusyou: str | None
    """通り略称"""

    @classmethod
    def from_node(cls, node: Node) -> "EkiTrack2":
        return cls(
            track_name=node.entries.get_required("TrackName"),
            track_ryakusyo=node.entries.get("TrackRyakusyou"),
            track_nobori_ryakusyou=node.entries.get("TrackNoboriRyakusyou"),
        )

    def to_node(self) -> Node:
        return Node(
            type="EkiTrack2",
            entries=EntryList(
                ("TrackName", self.track_name),
                ("TrackRyakusyou", self.track_ryakusyo),
                ("TrackNoboriRyakusyou", self.track_nobori_ryakusyou),
            ),
        )


@dataclass
class EkiTrack2Cont(TypedNode):
    """駅トラック2コンテナ`"""

    tracks: Sequence[EkiTrack2]

    @classmethod
    def from_node(cls, node: Node) -> "EkiTrack2Cont":
        return EkiTrack2Cont(
            tracks=[track for track in node.entries.node_lists[0] if isinstance(track, EkiTrack2)],
        )

    def to_node(self) -> Node:
        return Node(
            type="EkiTrack2Cont",
            entries=EntryList((None, NodeList(self.tracks))),
        )
