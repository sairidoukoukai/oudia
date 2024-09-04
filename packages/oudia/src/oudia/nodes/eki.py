from dataclasses import dataclass, field

from .node import Attributes, Children, Node, TypedNode


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
            ekimei=node.attributes.get_required("Ekimei"),
            ekijikokukeisiki=node.attributes.get_required(key="Ekijikokukeisiki"),
            ekikibo=node.attributes.get_required("Ekikibo"),
        )

    def to_node(self) -> Node:
        return Node(
            type="Eki",
            attributes=Attributes(
                ("Ekimei", self.ekimei),
                ("Ekijikokukeisiki", self.ekijikokukeisiki),
                ("Ekikibo", self.ekikibo),
            ),
            children=Children(),
            trailing_attributes=Attributes(),
        )
