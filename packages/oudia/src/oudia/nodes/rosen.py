from dataclasses import dataclass, field

from oudia.nodes.eki import Eki
from oudia.nodes.ressyasyubetsu import Ressyasyubetsu
from .node import EntryList, NodeList, Node, TypedNode


@dataclass
class Rosen(TypedNode):
    """路線"""

    rosenmei: str | None
    """路線名"""

    kudari_dia_alias: str | None
    """下りダイア別名（OuDiaSecond.1.04+）"""

    nobori_dia_alias: str | None
    """上りダイア別名（OuDiaSecond.1.04+）"""

    kiten_jikoku: str | None
    """起点時刻"""

    eki_list: NodeList[Eki] | None
    """駅リスト"""

    ressyasyubetsu_list: NodeList[Ressyasyubetsu] | None
    """列車種別リスト"""

    dia_list: NodeList[Node] | None
    """ダイアリスト"""

    diagram_dgr_y_zahyou_kyori_default: int | None
    """ダイヤグラムDGRY座標距離デフォルト"""

    enable_operation: bool | None
    """運用機能の有効無効（OuDiaSecond.1.03+）"""

    operation_cross_kiten_jikoku: bool | None
    """ダイヤグラム起点時刻を挟んで運用を接続する（OuDiaSecond.1.10+）"""

    kijun_dia_index: int | None
    """基準ダイヤインデックス"""

    comment: str | None
    """コメント"""

    @classmethod
    def from_node(cls, node: Node) -> "Rosen":
        return cls(
            rosenmei=node.entries.get("Rosenmei"),
            kudari_dia_alias=node.entries.get("KudariDiaAlias"),
            nobori_dia_alias=node.entries.get("NoboriDiaAlias"),
            kiten_jikoku=node.entries.get("KitenJikoku"),
            eki_list=node.entries.get_list(0, Eki),
            ressyasyubetsu_list=node.entries.get_list(1, Ressyasyubetsu),
            dia_list=node.entries.get_list(2, Node),
            diagram_dgr_y_zahyou_kyori_default=node.entries.get_int("DiagramDgrYZahyouKyoriDefault"),
            enable_operation=node.entries.get_bool("EnableOperation"),
            operation_cross_kiten_jikoku=node.entries.get_bool("OperationCrossKitenJikoku"),
            kijun_dia_index=node.entries.get_int("KijunDiaIndex"),
            comment=node.entries.get("Comment"),
        )

    def to_node(self) -> Node:
        return Node(
            type="Rosen",
            entries=EntryList(
                ("Rosenmei", self.rosenmei),
                ("KudariDiaAlias", self.kudari_dia_alias),
                ("NoboriDiaAlias", self.nobori_dia_alias),
                self.eki_list if self.eki_list else NodeList(Eki, []),
                self.ressyasyubetsu_list if self.ressyasyubetsu_list else NodeList(Ressyasyubetsu, []),
                self.dia_list if self.dia_list else NodeList(Node, []),
                ("KitenJikoku", self.kiten_jikoku),
                ("DiagramDgrYZahyouKyoriDefault", self.diagram_dgr_y_zahyou_kyori_default),
                ("OperationCrossKitenJikoku", self.operation_cross_kiten_jikoku),
                ("EnableOperation", self.enable_operation),
                ("KijunDiaIndex", self.kijun_dia_index),
                ("Comment", self.comment),
            ),
        )
