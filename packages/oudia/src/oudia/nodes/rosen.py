from dataclasses import dataclass, field
from ..helper import snake_case_to_CamelCase
from .node import Attributes, Node, TypedNode


@dataclass
class Rosen(TypedNode):
    """路線"""

    rosenmei: str | None = None
    """路線名"""

    kudari_dia_alias: str | None = None
    """下りダイア別名（OuDiaSecond.1.04+）"""

    nobori_dia_alias: str | None = None
    """上りダイア別名（OuDiaSecond.1.04+）"""

    kiten_jikoku: str | None = None
    """起点時刻"""

    diagram_dgr_y_zahyou_kyori_default: int | None = None
    """ダイヤグラムDGRY座標距離デフォルト"""

    enable_operation: bool | None = None
    """運用機能の有効無効（OuDiaSecond.1.03+）"""

    operation_cross_kiten_jikoku: int | None = None
    """ダイヤグラム起点時刻を挟んで運用を接続する（OuDiaSecond.1.10+）"""

    kijun_dia_index: int | None = None
    """基準ダイヤインデックス"""

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
            rosenmei=node.attributes.get("Rosenmei"),
            kudari_dia_alias=node.attributes.get("KudariDiaAlias"),
            nobori_dia_alias=node.attributes.get("NoboriDiaAlias"),
            kiten_jikoku=node.trailing_attributes.get("KitenJikoku"),
            diagram_dgr_y_zahyou_kyori_default=(
                int(v)
                if (v := node.trailing_attributes.get("DiagramDgrYZahyouKyoriDefault"))
                else None
            ),
            enable_operation=(
                bool(v)
                if (v := node.trailing_attributes.get("EnableOperation"))
                else None
            ),
            operation_cross_kiten_jikoku=(
                bool(v)
                if (v := node.trailing_attributes.get("OperationCrossKitenJikoku"))
                else None
            ),
            kijun_dia_index=(
                int(v) if (v := node.trailing_attributes.get("KijunDiaIndex")) else None
            ),
            comment=node.trailing_attributes.get("Comment"),
            _children=node.children,
        )

    def to_node(self) -> Node:
        return Node(
            type="Rosen",
            attributes=Attributes(
                ("Rosenmei", self.rosenmei),
                ("KudariDiaAlias", self.kudari_dia_alias),
                ("NoboriDiaAlias", self.nobori_dia_alias),
            ),
            trailing_attributes=Attributes(
                ("KitenJikoku", self.kiten_jikoku),
                (
                    "DiagramDgrYZahyouKyoriDefault",
                    (
                        str(self.diagram_dgr_y_zahyou_kyori_default)
                        if self.diagram_dgr_y_zahyou_kyori_default is not None
                        else None
                    ),
                ),
                (
                    "OperationCrossKitenJikoku",
                    (
                        ("1" if self.operation_cross_kiten_jikoku else "0")
                        if self.operation_cross_kiten_jikoku  # intentional as noted in http://oudiasecond.seesaa.net/article/481081211.html
                        else None
                    ),
                ),
                (
                    "EnableOperation",
                    (
                        ("1" if self.enable_operation else "0")
                        if self.enable_operation is not None
                        else None
                    ),
                ),
                (
                    "KijunDiaIndex",
                    (
                        str(self.kijun_dia_index)
                        if self.kijun_dia_index is not None
                        else None
                    ),
                ),
                ("Comment", self.comment),
            ),
        )

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Node):
            return self.to_node() == value
        if isinstance(value, Rosen):
            return self.rosenmei == value.rosenmei and self.children == value.children
        return False
