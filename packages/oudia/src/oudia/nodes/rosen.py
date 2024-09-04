from dataclasses import dataclass, field
from oudia.helper import snake_case_to_CamelCase
from oudia.types import Node, TypedNode


@dataclass
class Rosen(TypedNode):
    """路線"""

    rosenmei: str
    """路線名"""

    kudari_dia_alias: str | None = None
    """下りダイア別名（OuDiaSecond.1.04+）"""

    nobori_dia_alias: str | None = None
    """上りダイア別名（OuDiaSecond.1.04+）"""

    kiten_jikoku: str | None = None
    """起点時刻"""

    diagram_dgr_y_zahyou_kyori_default: int | None = None
    """ダイヤグラムDGRY座標距離デフォルト"""

    comment: str | None = None
    """コメント"""

    _children: list["Node | TypedNode"] = field(
        default_factory=list,
    )

    @property
    def children(self) -> list["Node | TypedNode"]:
        return self._children

    @staticmethod
    def from_node(node: Node) -> "Rosen":
        return Rosen(
            rosenmei=node.attributes["Rosenmei"],
            kudari_dia_alias=node.attributes.get("KudariDiaAlias"),
            nobori_dia_alias=node.attributes.get("NoboriDiaAlias"),
            kiten_jikoku=node.attributes.get("KitenJikoku"),
            diagram_dgr_y_zahyou_kyori_default=(
                int(v)
                if (v := node.attributes.get("DiagramDgrYZahyouKyoriDefault"))
                else None
            ),
            comment=node.attributes.get("Comment"),
            _children=node.children,
        )

    def to_node(self) -> Node:
        return Node(
            type="Rosen",
            attributes={
                snake_case_to_CamelCase(k): v
                for k, v in self.__dict__.items()
                if k != "_children" and v
            },
            children=self.children,
        )

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Node):
            return self.to_node() == value
        if isinstance(value, Rosen):
            return self.rosenmei == value.rosenmei and self.children == value.children
        return False
