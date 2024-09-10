from dataclasses import dataclass
from .node import EntryList, Node, TypedNode


@dataclass(kw_only=True)
class OuterTerminal(TypedNode):
    """路線外発着駅名"""

    outer_terminal_ekimei: str | None = None
    """路線外発着駅名"""

    outer_terminal_jikoku_ryaku: str | None = None
    """路線外発着駅名の時刻表ビューにおける略称"""

    outer_terminal_dia_ryaku: str | None = None
    """路線外発着駅名のダイアグラムビューにおける略称"""

    @classmethod
    def from_node(cls, node: Node) -> "OuterTerminal":
        return cls(
            outer_terminal_ekimei=node.entries.get("OuterTerminalEkimei"),
            outer_terminal_jikoku_ryaku=node.entries.get("OuterTerminalJikokuRyaku"),
            outer_terminal_dia_ryaku=node.entries.get("OuterTerminalDiaRyaku"),
        )

    def to_node(self) -> Node:
        return Node(
            type="OuterTerminal",
            entries=EntryList(
                ("OuterTerminalEkimei", self.outer_terminal_ekimei),
                ("OuterTerminalJikokuRyaku", self.outer_terminal_jikoku_ryaku),
                ("OuterTerminalDiaRyaku", self.outer_terminal_dia_ryaku),
            ),
        )
