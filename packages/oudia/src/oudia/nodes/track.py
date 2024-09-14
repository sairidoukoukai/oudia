"""駅番線を扱うためのモジュールです。"""

from dataclasses import dataclass, field
from typing import Sequence  # TODO: Remove unused variables
from .node import EntryList, NodeList, Node, TypedNode


@dataclass(kw_only=True)
class EkiTrack2(TypedNode):
    """駅番線"""

    track_name: str
    """番線名"""

    track_ryakusyou: str | None = None
    """番線略称"""

    track_nobori_ryakusyou: str | None = None
    """番線略称（上り）"""

    @classmethod
    def from_node(cls, node: Node) -> "EkiTrack2":
        """ノードから駅番線を生成します。"""
        return cls(
            track_name=node.entries.get_required("TrackName"),
            track_ryakusyou=node.entries.get("TrackRyakusyou"),
            track_nobori_ryakusyou=node.entries.get("TrackNoboriRyakusyou"),
        )

    def to_node(self) -> Node:
        """駅番線をノードに変換します。"""
        return Node(
            type="EkiTrack2",
            entries=EntryList(
                ("TrackName", self.track_name),
                ("TrackRyakusyou", self.track_ryakusyou),
                ("TrackNoboriRyakusyou", self.track_nobori_ryakusyou),
            ),
        )


@dataclass(kw_only=True)
class EkiTrack2Cont(TypedNode):
    """駅番線コンテナ"""

    tracks: list[EkiTrack2]
    """番線リスト"""

    @classmethod
    def from_node(cls, node: Node) -> "EkiTrack2Cont":
        """ノードから駅番線コンテナを生成します。"""
        return EkiTrack2Cont(
            tracks=node.entries.get_list_by_type(EkiTrack2),
        )

    def to_node(self) -> Node:
        """駅番線コンテナをノードに変換します。"""
        return Node(
            type="EkiTrack2Cont",
            entries=EntryList(NodeList(EkiTrack2, self.tracks)),
        )
