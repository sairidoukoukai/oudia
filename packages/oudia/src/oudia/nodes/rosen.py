from dataclasses import dataclass, field
from .node import Attributes, Children, Node, TypedNode


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

    operation_cross_kiten_jikoku: bool | None = None
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
            diagram_dgr_y_zahyou_kyori_default=node.trailing_attributes.get_int("DiagramDgrYZahyouKyoriDefault"),
            enable_operation=node.trailing_attributes.get_bool("EnableOperation"),
            operation_cross_kiten_jikoku=node.trailing_attributes.get_bool("OperationCrossKitenJikoku"),
            kijun_dia_index=node.trailing_attributes.get_int("KijunDiaIndex"),
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
                ("DiagramDgrYZahyouKyoriDefault", self.diagram_dgr_y_zahyou_kyori_default),
                ("OperationCrossKitenJikoku", self.operation_cross_kiten_jikoku),
                ("EnableOperation", self.enable_operation),
                ("KijunDiaIndex", self.kijun_dia_index),
                ("Comment", self.comment),
            ),
            children=Children(self.children),
        )
