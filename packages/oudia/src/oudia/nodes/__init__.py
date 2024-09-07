from typing import Type

from .eki import Eki
from .rosen import Rosen
from .ressyasyubetsu import Ressyasyubetsu
from .track import EkiTrack2, EkiTrack2Cont
from .node import Node, TypedNode
from .root import OuDia, FileType
from .disp_prop import DispProp
from .crossing_check_rule import CrossingCheckRule
from .outer_terminal import OuterTerminal
from .ressya import Ressya
from .dia import Dia, Kudari, Nobori
from .window_placement import WindowPlacement, ChildWindow


TYPE_TO_NODE: dict[str, Type[TypedNode]] = {
    "Root": OuDia,
    "Rosen": Rosen,
    "Eki": Eki,
    "Ressyasyubetsu": Ressyasyubetsu,
    "EkiTrack2": EkiTrack2,
    "EkiTrack2Cont": EkiTrack2Cont,
    "CrossingCheckRule": CrossingCheckRule,
    "DispProp": DispProp,
    "OuterTerminal": OuterTerminal,
    "Ressya": Ressya,
    "Dia": Dia,
    "Nobori": Nobori,
    "Kudari": Kudari,
    "WindowPlacement": WindowPlacement,
    "ChildWindow": ChildWindow,
}


def type_to_typed_node_type(type: str | None) -> Type[TypedNode] | None:
    return TYPE_TO_NODE.get(type) if type else None


__all__ = [
    "TYPE_TO_NODE",
    "Eki",
    "Rosen",
    "Node",
    "TypedNode",
    "OuDia",
    "FileType",
    "Ressyasyubetsu",
    "EkiTrack2",
    "EkiTrack2Cont",
    "DispProp",
    "CrossingCheckRule",
    "OuterTerminal",
    "Ressya",
    "Nobori",
    "Kudari",
    "WindowPlacement",
    "ChildWindow",
    "Dia",
]
