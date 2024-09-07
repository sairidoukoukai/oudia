from dataclasses import dataclass, field
from typing import Sequence
from .node import EntryList, NodeList, Node, TypedNode


@dataclass
class EkiTrack2(TypedNode):
    """駅トラック2"""

    track_name: str
    """トラック名"""

    track_ryakusyo: str | None = None
    """トラック略称"""

    track_nobori_ryakusyou: str | None = None
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
    """駅トラック2コンテナ"""

    tracks: list[EkiTrack2]
    """トラックリスト"""

    @classmethod
    def from_node(cls, node: Node) -> "EkiTrack2Cont":
        return EkiTrack2Cont(
            tracks=node.entries.get_list_by_type(EkiTrack2),
        )

    def to_node(self) -> Node:
        return Node(
            type="EkiTrack2Cont",
            entries=EntryList(NodeList(EkiTrack2, self.tracks)),
        )
