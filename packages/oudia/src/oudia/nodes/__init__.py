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
}

__all__ = [
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
    "TYPE_TO_NODE",
]
