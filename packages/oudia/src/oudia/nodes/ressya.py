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
        # add operations
        for key, value in node.entries.properties:
            if key.startswith("Operation"):
                operation_type = OperationType(key[-1])
                id = int(key[9:-1])

                if id >= len(eki_jikoku_plain) or not (current_eki_jikoku := eki_jikoku_plain[id]):
                    raise ValueError(f"Invalid operation: Operation {id} {operation_type}")

                match operation_type:
                    case OperationType.AFTER:
                        current_eki_jikoku.after_operation_list.append(AfterOperation.from_str(value))
                    case OperationType.BEFORE:
                        current_eki_jikoku.before_operation_list.append(BeforeOperation.from_str(value))

        return cls(
            houkou=node.entries.get("Houkou"),
            syubetsu=node.entries.get_int("Syubetsu"),
            ressyabangou=node.entries.get("Ressyabangou"),
            ressyamei=node.entries.get("Ressyamei"),
            eki_jikoku_list=eki_jikoku_plain,
            bikou=node.entries.get("Bikou"),
        )

    def to_node(self) -> Node:
        operation_entries: list[tuple[str, str]] = []

        for i, eki_jikoku in enumerate(self.eki_jikoku_list):
            if not eki_jikoku:
                continue
            for operation in eki_jikoku.after_operation_list:
                operation_entries.append((f"Operation{i}A", str(operation)))
            for operation in eki_jikoku.before_operation_list:
                operation_entries.append((f"Operation{i}B", str(operation)))

        return Node(
            type="Ressya",
            entries=EntryList(
                ("Houkou", self.houkou),
                ("Syubetsu", self.syubetsu),
                ("Ressyabangou", self.ressyabangou),
                ("Ressyamei", self.ressyamei),
                ("EkiJikoku", ",".join(str(x) if x else "" for x in self.eki_jikoku_list)),
                *operation_entries,
                ("Bikou", self.bikou),
            ),
        )
