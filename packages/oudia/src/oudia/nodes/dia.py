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
            type="Kudari",
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

    main_back_color_index: int | None = None
    """メイン背景色のインデックス"""

    sub_back_color_index: int | None = None
    """サブ背景色のインデックス"""

    back_pattern_index: int | None = None
    """背景パターンのインデックス"""

    @classmethod
    def from_node(cls, node: Node) -> "Dia":
        return cls(
            dia_name=node.entries.get_required("DiaName"),
            main_back_color_index=node.entries.get_int("MainBackColorIndex"),
            sub_back_color_index=node.entries.get_int("SubBackColorIndex"),
            back_pattern_index=node.entries.get_int("BackPatternIndex"),
            kudari=node.entries.get_list_by_type(Kudari),
            nobori=node.entries.get_list_by_type(Nobori),
        )

    def to_node(self) -> Node:
        return Node(
            type="Dia",
            entries=EntryList(
                ("DiaName", self.dia_name),
                ("MainBackColorIndex", self.main_back_color_index),
                ("SubBackColorIndex", self.sub_back_color_index),
                ("BackPatternIndex", self.back_pattern_index),
                NodeList(Kudari, self.kudari),
                NodeList(Nobori, self.nobori),
            ),
        )
