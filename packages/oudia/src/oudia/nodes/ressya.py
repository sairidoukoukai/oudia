"""列車を扱うためのモジュールです。"""

import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from oudia.dia.eki_jikoku import EkiJikoku
from oudia.dia.operation import AfterOperationFactory, BeforeOperationFactory, OperationBase

from .node import EntryList, Node, TypedNode


class OperationType(Enum):
    """作業の種別"""

    # TODO: This should be in oudia.dia.operation

    AFTER = "A"
    BEFORE = "B"


OPERATION_KEY = re.compile(r"Operation\d+[AB](\.\d+[AB])?")
"""作業の属性名。`Operation3B`・`Operation3B.0A`の形を取る。"""


@dataclass(kw_only=True)
class Ressya(TypedNode):
    """列車"""

    eki_jikoku_list: list[EkiJikoku | None]
    """駅時刻"""

    houkou: str | None = None
    """方向（上り・下り）"""

    syubetsu: int | None = None
    """種別"""

    unyoubangou: str | None = None
    """運用番号"""

    ressyabangou: str | None = None
    """列車番号"""

    ressyamei: str | None = None
    """列車名"""

    gousuu: str | None = None
    """号数"""

    bikou: str | None = None
    """備考"""

    syubetsu_change: bool | None = None
    """種別変更の有無（OuDiaSecond.1.09以前）"""

    ressya_track: str | None = None
    """駅ごとの番線（OuDiaSecond.1.05以前。以降は駅時刻に含まれる）"""

    operation_number: str | None = None
    """運用番号（OuDiaSecond.1.09以前）"""

    canceled: bool | None = None
    """運休かどうか"""

    @classmethod
    def from_node(cls, node: Node) -> "Ressya":
        """ノードから列車を生成します。"""
        eki_jikoku_str = node.entries.get("EkiJikoku")
        eki_jikoku_plain = (
            [EkiJikoku.from_str(x) if x else None for x in eki_jikoku_str.split(",")]
            if eki_jikoku_str is not None
            else []
        )

        # [ekijikoku_index, list[Operation]]
        parent_before_operation_list: defaultdict[int, list[OperationBase]] = defaultdict(list)
        parent_after_operation_list: defaultdict[int, list[OperationBase]] = defaultdict(list)

        for key, value in node.entries.properties:
            if OPERATION_KEY.fullmatch(key):
                indicator = key[9:]  # '73B' / '73B.0A'
                operation_type = OperationType(indicator[-1])  # 'A' / 'B' -> OperationType.AFTER / OperationType.BEFORE

                if "." not in key:
                    # Operation73B
                    id = int(indicator[:-1])  # 73

                    if id >= len(eki_jikoku_plain):
                        raise ValueError(f"Invalid operation: Operation {id} {operation_type}")

                    for operation_str in value.split(","):
                        match operation_type:
                            case OperationType.BEFORE:
                                parent_before_operation_list[id].append(BeforeOperationFactory.from_str(operation_str))
                            case OperationType.AFTER:
                                parent_after_operation_list[id].append(AfterOperationFactory.from_str(operation_str))
                else:
                    # Operation73B.0A
                    parent_indicator, child_indicator = indicator.split(".")  # '73B', '0A'
                    parent_id = int(parent_indicator[:-1])  # 73
                    child_id = int(child_indicator[:-1])  # 0
                    parent_operation_type = OperationType(parent_indicator[-1])

                    if parent_id not in parent_before_operation_list and parent_id not in parent_after_operation_list:
                        raise ValueError(f"Invalid operation: Operation {parent_id} {operation_type}")

                    for v in value.split(","):
                        match parent_operation_type, operation_type:
                            case OperationType.BEFORE, OperationType.BEFORE:
                                parent_before_operation_list[parent_id][child_id].before_operation_list.append(
                                    BeforeOperationFactory.from_str(text=v)
                                )
                            case OperationType.BEFORE, OperationType.AFTER:
                                parent_before_operation_list[parent_id][child_id].after_operation_list.append(
                                    AfterOperationFactory.from_str(v)
                                )

                            case OperationType.AFTER, OperationType.BEFORE:
                                parent_after_operation_list[parent_id][child_id].before_operation_list.append(
                                    BeforeOperationFactory.from_str(v)
                                )
                            case OperationType.AFTER, OperationType.AFTER:
                                parent_after_operation_list[parent_id][child_id].after_operation_list.append(
                                    AfterOperationFactory.from_str(v)
                                )

        for i, before_operation_list in parent_before_operation_list.items():
            if (current_eki_jikoku := eki_jikoku_plain[i]) is None:
                raise ValueError(f"Invalid before operation: Ekijikoku[{i}] does not exist")
            for before_operation in before_operation_list:
                current_eki_jikoku.before_operation_list.append(before_operation)

        for i, after_operation_list in parent_after_operation_list.items():
            if (current_eki_jikoku := eki_jikoku_plain[i]) is None:
                raise ValueError(f"Invalid after operation: Ekijikoku[{i}] does not exist")
            for after_operation in after_operation_list:
                current_eki_jikoku.after_operation_list.append(after_operation)

        return cls(
            houkou=node.entries.get("Houkou"),
            syubetsu=node.entries.get_int("Syubetsu"),
            ressyabangou=node.entries.get("Ressyabangou"),
            ressyamei=node.entries.get("Ressyamei"),
            unyoubangou=node.entries.get("Unyoubangou"),
            gousuu=node.entries.get("Gousuu"),
            eki_jikoku_list=eki_jikoku_plain,
            bikou=node.entries.get("Bikou"),
            syubetsu_change=node.entries.get_bool("SyubetsuChange"),
            ressya_track=node.entries.get("RessyaTrack"),
            operation_number=node.entries.get("OperationNumber"),
            canceled=node.entries.get_bool("Canceled"),
        )

    def to_node(self) -> Node:
        """列車をノードに変換します。"""
        operation_entries: list[tuple[str, str]] = []

        for i, eki_jikoku in enumerate(self.eki_jikoku_list):
            if not eki_jikoku:
                continue

            if eki_jikoku.before_operation_list:
                operation_entry_value = ",".join([str(x) for x in eki_jikoku.before_operation_list if x])
                operation_entries.append((f"Operation{i}B", operation_entry_value))

                for j, operation in enumerate(eki_jikoku.before_operation_list):
                    if operation.before_operation_list:
                        operation_entries.append(
                            (
                                f"Operation{i}B.{j}B",
                                ",".join(str(object=child) for child in operation.before_operation_list),
                            )
                        )
                    if operation.after_operation_list:
                        operation_entries.append(
                            (
                                f"Operation{i}B.{j}A",
                                ",".join(str(object=child) for child in operation.after_operation_list),
                            )
                        )

            if eki_jikoku.after_operation_list:
                operation_entry_value = ",".join([str(x) for x in eki_jikoku.after_operation_list if x])
                operation_entries.append((f"Operation{i}A", operation_entry_value))

                for j, operation in enumerate(eki_jikoku.after_operation_list):
                    if operation.before_operation_list:
                        operation_entries.append(
                            (
                                f"Operation{i}A.{j}B",
                                ",".join(str(object=child) for child in operation.before_operation_list),
                            )
                        )
                    if operation.after_operation_list:
                        operation_entries.append(
                            (
                                f"Operation{i}A.{j}A",
                                ",".join(str(object=child) for child in operation.after_operation_list),
                            )
                        )

        return Node(
            type="Ressya",
            entries=EntryList(
                ("Houkou", self.houkou),
                ("Syubetsu", self.syubetsu),
                ("Ressyabangou", self.ressyabangou),
                ("Ressyamei", self.ressyamei),
                ("Unyoubangou", self.unyoubangou),
                ("Gousuu", self.gousuu),
                ("SyubetsuChange", self.syubetsu_change),
                (
                    ("EkiJikoku", ",".join(str(x) if x else "" for x in self.eki_jikoku_list))
                    if self.eki_jikoku_list
                    else ("EkiJikoku", None)
                ),
                ("RessyaTrack", self.ressya_track),
                *operation_entries,
                ("Bikou", self.bikou),
                ("Canceled", self.canceled),
                ("OperationNumber", self.operation_number),
            ),
        )
