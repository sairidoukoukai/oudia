from dataclasses import dataclass, field
from .node import Node, TypedNode


@dataclass
class Eki(TypedNode):
    """駅"""

    ekimei: str
    """駅名"""

    ekijikokukeisiki: str
    """駅時刻形式"""

    ekikibo: str
    """駅規模"""

    _children: list["Node | TypedNode"] = field(default_factory=list)

    @property
    def children(self) -> list["Node | TypedNode"]:
        return self._children

    @staticmethod
    def from_node(node: Node) -> "Eki":
        return Eki(
            ekimei=node.attributes["Ekimei"],
            ekijikokukeisiki=node.attributes["Ekijikokukeisiki"],
            ekikibo=node.attributes["Ekikibo"],
        )

    def to_node(self) -> Node:
        return Node(
            type="Eki",
            attributes={
                "Ekimei": self.ekimei,
                "Ekijikokukeisiki": self.ekijikokukeisiki,
                "Ekikibo": self.ekikibo,
            },
        )
