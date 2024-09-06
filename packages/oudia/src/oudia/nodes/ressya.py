from dataclasses import dataclass
from oudia.dia.eki_jikoku import EkiJikoku

from .node import EntryList, Node, TypedNode


@dataclass
class Ressya(TypedNode):
    """列車"""

    eki_jikoku_list: list[EkiJikoku]
    """駅時刻"""

    houkou: str | None = None
    """方向（上り・下り）"""

    syubetsu: int | None = None
    """種別"""

    ressyabangou: str | None = None
    """列車番号"""

    ressyamei: str | None = None
    """列車名"""

    gousuu: str | None = None
    """号数"""

    @classmethod
    def from_node(cls, node: Node) -> "Ressya":
        return cls(
            houkou=node.entries.get("Houkou"),
            syubetsu=node.entries.get_int("Syubetsu"),
            ressyabangou=node.entries.get("Ressyabangou"),
            ressyamei=node.entries.get("Ressyamei"),
            eki_jikoku_list=list(
                map(EkiJikoku.from_str, [x for x in node.entries.get_required("EkiJikoku").split(",") if x])
            ),
        )

    def to_node(self) -> Node:
        return Node(
            type="Ressya",
            entries=EntryList(
                ("Houkou", self.houkou),
                ("Syubetsu", self.syubetsu),
                ("Ressyabangou", self.ressyabangou),
                ("Ressyamei", self.ressyamei),
                ("EkiJikoku", ",".join(map(str, self.eki_jikoku_list))),
            ),
        )
