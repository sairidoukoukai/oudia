from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from oudia.dia.eki_jikoku import EkiJikoku
from oudia.dia.operation import AfterOperation, BeforeOperation

from .node import EntryList, Node, TypedNode


class OperationType(Enum):
    AFTER = "A"
    BEFORE = "B"


@dataclass
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

    @classmethod
    def from_node(cls, node: Node) -> "Ressya":
        eki_jikoku_plain = [
            EkiJikoku.from_str(x) if x else None for x in node.entries.get_required("EkiJikoku").split(",")
        ]

        # [ekijikoku_index, list[Operation]]
        parent_before_operations: defaultdict[int, list[BeforeOperation]] = defaultdict(list)
        parent_after_operations: defaultdict[int, list[AfterOperation]] = defaultdict(list)

        for key, value in node.entries.properties:
            if key.startswith("Operation"):
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
                                parent_before_operations[id].append(BeforeOperation.from_str(operation_str))
                            case OperationType.AFTER:
                                parent_after_operations[id].append(AfterOperation.from_str(operation_str))
                else:
                    # Operation73B.0A
                    parent_indicator, child_indicator = indicator.split(".")  # '73B', '0A'
                    parent_id = int(parent_indicator[:-1])  # 73
                    child_id = int(child_indicator[:-1])  # 0
                    parent_operation_type = OperationType(parent_indicator[-1])

                    if parent_id not in parent_before_operations and parent_id not in parent_after_operations:
                        raise ValueError(f"Invalid operation: Operation {parent_id} {operation_type}")

                    for v in value.split(","):
                        match parent_operation_type, operation_type:
                            case OperationType.BEFORE, OperationType.BEFORE:
                                parent_before_operations[parent_id][child_id].before_operation_list.append(
                                    BeforeOperation.from_str(text=v)
                                )
                            case OperationType.BEFORE, OperationType.AFTER:
                                parent_before_operations[parent_id][child_id].after_operation_list.append(
                                    AfterOperation.from_str(v)
                                )

                            case OperationType.AFTER, OperationType.BEFORE:
                                parent_after_operations[parent_id][child_id].before_operation_list.append(
                                    BeforeOperation.from_str(v)
                                )
                            case OperationType.AFTER, OperationType.AFTER:
                                parent_after_operations[parent_id][child_id].after_operation_list.append(
                                    AfterOperation.from_str(v)
                                )

        for i, before_operations in parent_before_operations.items():
            if (current_eki_jikoku := eki_jikoku_plain[i]) is None:
                raise ValueError(f"Invalid before operation: Ekijikoku[{i}] does not exist")
            for before_operation in before_operations:
                current_eki_jikoku.before_operation_list.append(before_operation)

        for i, after_operations in parent_after_operations.items():
            if (current_eki_jikoku := eki_jikoku_plain[i]) is None:
                raise ValueError(f"Invalid after operation: Ekijikoku[{i}] does not exist")
            for after_operation in after_operations:
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
        )

    def to_node(self) -> Node:
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
                ("EkiJikoku", ",".join(str(x) if x else "" for x in self.eki_jikoku_list)),
                *operation_entries,
                ("Bikou", self.bikou),
            ),
        )
