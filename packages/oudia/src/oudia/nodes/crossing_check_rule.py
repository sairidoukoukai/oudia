from dataclasses import dataclass, field
from .node import EntryList, Node, TypedNode


@dataclass(kw_only=True)
class CrossingCheckRule(TypedNode):
    """交差支障チェックルール"""

    caption: str | None = None
    """説明文"""

    enable: bool | None = None
    """有効・無効"""

    headway_second: int | None = None
    """時隔上限(秒)"""

    headway_second_minimum: int | None = None
    """時隔下限(秒)"""

    before_from_track_content_cont: str | None = None
    """前動作の移動前番線"""

    before_to_track_content_cont: str | None = None
    """前動作の移動後番線"""

    before_is_arrival: bool | None = None
    """前動作の到着・出発 """

    before_is_tsuuka: bool | None = None
    """前動作の通過・停車"""

    after_from_track_content_cont: str | None = None
    """後動作の移動前番線"""

    after_to_track_content_cont: str | None = None
    """後動作の移動後番線"""

    after_is_arrival: bool | None = None
    """後動作の到着・出発"""

    after_is_tsuuka: bool | None = None
    """後動作の通過・停車"""

    @classmethod
    def from_node(cls, node: Node) -> "CrossingCheckRule":
        return cls(
            caption=node.entries.get("Caption"),
            enable=node.entries.get_bool("Enable"),
            headway_second=node.entries.get_int("HeadwaySecond"),
            headway_second_minimum=node.entries.get_int("HeadwaySecondMinimum"),
            before_from_track_content_cont=node.entries.get("BeforeFromTrackContentCont"),
            before_to_track_content_cont=node.entries.get("BeforeToTrackContentCont"),
            before_is_arrival=node.entries.get_bool("BeforeIsArrival"),
            before_is_tsuuka=node.entries.get_bool("BeforeIsTsuuka"),
            after_from_track_content_cont=node.entries.get("AfterFromTrackContentCont"),
            after_to_track_content_cont=node.entries.get("AfterToTrackContentCont"),
            after_is_arrival=node.entries.get_bool("AfterIsArrival"),
            after_is_tsuuka=node.entries.get_bool("AfterIsTsuuka"),
        )

    def to_node(self) -> Node:
        return Node(
            type="CrossingCheckRule",
            entries=EntryList(
                ("Caption", self.caption),
                ("Enable", self.enable),
                ("HeadwaySecond", self.headway_second),
                ("HeadwaySecondMinimum", self.headway_second_minimum),
                ("BeforeFromTrackContentCont", self.before_from_track_content_cont),
                ("BeforeToTrackContentCont", self.before_to_track_content_cont),
                ("BeforeIsArrival", self.before_is_arrival),
                ("BeforeIsTsuuka", self.before_is_tsuuka),
                ("AfterFromTrackContentCont", self.after_from_track_content_cont),
                ("AfterToTrackContentCont", self.after_to_track_content_cont),
                ("AfterIsArrival", self.after_is_arrival),
                ("AfterIsTsuuka", self.after_is_tsuuka),
            ),
        )
