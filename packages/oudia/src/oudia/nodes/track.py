from dataclasses import dataclass, field

from .node import Attributes, Children, Node, TypedNode


@dataclass
class EkiTrack2(TypedNode):
    """駅トラック2"""

    track_name: str
    """トラック名"""

    track_ryakusyo: str | None
    """トラック略称"""

    _children: list["Node | TypedNode"] = field(default_factory=list)

    @property
    def children(self) -> list["Node | TypedNode"]:
        return self._children

    @classmethod
    def from_node(cls, node: Node) -> "EkiTrack2":
        return cls(
            track_name=node.attributes.get_required("TrackName"),
            track_ryakusyo=node.attributes.get("TrackRyakusyou"),
            _children=node.children,
        )

    def to_node(self) -> Node:
        return Node(
            type="EkiTrack2",
            attributes=Attributes(
                ("TrackName", self.track_name),
                ("TrackRyakusyou", self.track_ryakusyo),
            ),
            children=Children(),
            trailing_attributes=Attributes(),
        )


@dataclass
class EkiTrack2Cont(TypedNode):
    """駅トラック2コンテナ`"""

    _children: list["Node | TypedNode"] = field(default_factory=list)

    @property
    def children(self) -> list["Node | TypedNode"]:
        return self._children

    @classmethod
    def from_node(cls, node: Node) -> "EkiTrack2Cont":
        return EkiTrack2Cont(
            _children=node.children,
        )

    def to_node(self) -> Node:
        return Node(
            type="EkiTrack2Cont",
            attributes=Attributes(),
            children=Children(self.children),
            trailing_attributes=Attributes(),
        )
