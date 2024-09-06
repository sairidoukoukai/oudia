from dataclasses import dataclass, field

from .node import EntryList, Node, TypedNode


@dataclass
class Ressya(TypedNode):
    """列車"""

    houkou: str | None = None
    """方向（上り・下り）"""

    syubetsu: int | None = None
    """種別"""

    ressyabangou: str | None = None
    """列車番号"""

    ressyamei: str | None = None
    """列車名"""

    eki_jikoku: str | None = None
    """駅時刻"""

    @classmethod
    def from_node(cls, node: Node) -> "Ressya":
        return cls(
            houkou=node.entries.get("Houkou"),
            syubetsu=node.entries.get_int("Syubetsu"),
            ressyabangou=node.entries.get("Ressyabangou"),
            ressyamei=node.entries.get("Ressyamei"),
            eki_jikoku=node.entries.get("EkiJikoku"),
        )

    def to_node(self) -> Node:
        return Node(
            type="Rosen",
            entries=EntryList(
                ("Houkou", self.houkou),
                ("Syubetsu", self.syubetsu),
                ("Ressyabangou", self.ressyabangou),
                ("Ressyamei", self.ressyamei),
                ("EkiJikoku", self.eki_jikoku),
            ),
        )
