"""路線を扱うためのモジュールです。"""

from dataclasses import dataclass

from oudia.nodes.dia import Dia
from oudia.nodes.eki import Eki
from oudia.nodes.ressyasyubetsu import Ressyasyubetsu
from .node import EntryList, NodeList, Node, TypedNode


@dataclass(kw_only=True)
class Rosen(TypedNode):
    """路線"""

    eki_list: NodeList[Eki]
    """駅リスト"""

    ressyasyubetsu_list: NodeList[Ressyasyubetsu]
    """列車種別リスト"""

    dia_list: NodeList[Dia]
    """ダイアリスト"""

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

    enable_operation: int | None = None
    """運用機能の有効無効（OuDiaSecond.1.03+）"""

    operation_number_reverse: bool | None = None
    """運用番号順を反転するかどうか"""

    operation_cross_kiten_jikoku: bool | None = None
    """ダイヤグラム起点時刻を挟んで運用を接続する（OuDiaSecond.1.10+）"""

    disable_hidden_syubetsu: bool | None = None
    """隠した種別を使わないかどうか"""

    kijun_dia_index: int | None = None
    """基準ダイヤインデックス"""

    comment: str | None = None
    """コメント"""

    @classmethod
    def from_node(cls, node: Node) -> "Rosen":
        """ノードから路線を生成します。"""
        return cls(
            rosenmei=node.entries.get("Rosenmei"),
            kudari_dia_alias=node.entries.get("KudariDiaAlias"),
            nobori_dia_alias=node.entries.get("NoboriDiaAlias"),
            kiten_jikoku=node.entries.get("KitenJikoku"),
            eki_list=node.entries.get_list_by_type(Eki),
            ressyasyubetsu_list=node.entries.get_list_by_type(Ressyasyubetsu),
            dia_list=node.entries.get_list_by_type(Dia),
            diagram_dgr_y_zahyou_kyori_default=node.entries.get_int("DiagramDgrYZahyouKyoriDefault"),
            enable_operation=node.entries.get_int("EnableOperation"),
            operation_number_reverse=node.entries.get_bool("OperationNumberReverse"),
            operation_cross_kiten_jikoku=node.entries.get_bool("OperationCrossKitenJikoku"),
            kijun_dia_index=node.entries.get_int("KijunDiaIndex"),
            disable_hidden_syubetsu=node.entries.get_bool("DisableHiddenSyubetsu"),
            comment=node.entries.get("Comment"),
        )

    def to_node(self) -> Node:
        """路線をノードに変換します。"""
        return Node(
            type="Rosen",
            entries=EntryList(
                ("Rosenmei", self.rosenmei),
                ("KudariDiaAlias", self.kudari_dia_alias),
                ("NoboriDiaAlias", self.nobori_dia_alias),
                self.eki_list,
                self.ressyasyubetsu_list,
                self.dia_list,
                ("KitenJikoku", self.kiten_jikoku),
                ("DiagramDgrYZahyouKyoriDefault", self.diagram_dgr_y_zahyou_kyori_default),
                ("EnableOperation", self.enable_operation),
                ("OperationNumberReverse", self.operation_number_reverse),
                ("OperationCrossKitenJikoku", self.operation_cross_kiten_jikoku),
                ("KijunDiaIndex", self.kijun_dia_index),
                ("DisableHiddenSyubetsu", self.disable_hidden_syubetsu),
                ("Comment", self.comment),
            ),
        )
