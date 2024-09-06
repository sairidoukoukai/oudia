from dataclasses import dataclass

from oudia.nodes import Ressya

from .node import EntryList, Node, TypedNode, NodeList


@dataclass
class Kudari(TypedNode):
    """下り"""

    ressya_list: NodeList[Ressya]

    @classmethod
    def from_node(cls, node: Node) -> "Kudari":
        return cls(
            ressya_list=node.entries.get_list_by_type(Ressya),
        )

    def to_node(self) -> Node:
        return Node(
            type="Rosen",
            entries=EntryList(
                NodeList(Ressya, self.ressya_list),
            ),
        )


@dataclass
class Nobori(TypedNode):
    """上り"""

    ressya_list: NodeList[Ressya]

    @classmethod
    def from_node(cls, node: Node) -> "Nobori":
        return cls(
            ressya_list=node.entries.get_list_by_type(Ressya),
        )

    def to_node(self) -> Node:
        return Node(
            type="Nobori",
            entries=EntryList(
                NodeList(Ressya, self.ressya_list),
            ),
        )


@dataclass
class Dia(TypedNode):
    """ダイヤ"""

    dia_name: str
    """ダイヤ名"""

    kudari: NodeList[Kudari]
    """下り"""

    nobori: NodeList[Nobori]
    """上り"""

    @classmethod
    def from_node(cls, node: Node) -> "Dia":
        return cls(
            dia_name=node.entries.get_required("DiaName"),
            kudari=node.entries.get_list_by_type(Kudari),
            nobori=node.entries.get_list_by_type(Nobori),
        )

    def to_node(self) -> Node:
        return Node(
            type="Dia",
            entries=EntryList(
                ("DiaName", self.dia_name),
                NodeList(Kudari, self.kudari),
                NodeList(Nobori, self.nobori),
            ),
        )
