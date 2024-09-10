from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, ClassVar, Self, Type

from oudia.dia.jikoku import Hour, Jikoku, JikokuConv, Second

JIKOKU_CONV = JikokuConv(no_colon=True, hour=Hour.ZERO_TO_NONE, second=Second.NOT_IF_ZERO)


@dataclass(kw_only=True)
class OperationBase(ABC):
    before_operation_list: list[Self] = field(default_factory=list)
    after_operation_list: list[Self] = field(default_factory=list)

    @classmethod
    @abstractmethod
    def from_str(cls, text: str) -> Self:
        pass  # pragma: no cover

    @abstractmethod
    def __str__(self) -> str:
        pass  # pragma: no cover


# region BeforeOperation


class BOperation(Enum):
    """作業種別"""

    SHUNT = 0
    """入換"""

    CONNECT = 1
    """増結"""

    RELEASE = 2
    """解結"""

    OUT = 3
    """出区"""

    OUTER = 4
    """路線外始発"""

    JUNCTION = 5
    """前列車接続"""

    NUMBER_CHANGE = 6
    """運用番号変更"""


@dataclass(kw_only=True)
class BeforeOperationShunt(OperationBase):
    """前作業（入換）"""

    OPERATION_TYPE: ClassVar[BOperation] = BOperation.SHUNT

    shunt_track_index: int
    """入換トラック番号"""

    hatsu_jikoku: Jikoku
    """発時刻"""

    chaku_jikoku: Jikoku
    """着時刻"""

    is_display_chaku_jikoku: bool
    """着時刻表示の有無"""

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        parts = rest.split("$")
        shunt_track_index = int(parts[0])
        hatsu_jikoku = JIKOKU_CONV.decode(parts[1].split("/")[0])
        chaku_jikoku = JIKOKU_CONV.decode(parts[1].split("/")[1]) if "/" in parts[1] else Jikoku(None)
        is_display_chaku_jikoku = parts[2] == "1"  # TODO: Add special function to convert between boolean

        return cls(
            shunt_track_index=shunt_track_index,
            hatsu_jikoku=hatsu_jikoku,
            chaku_jikoku=chaku_jikoku,
            is_display_chaku_jikoku=is_display_chaku_jikoku,
        )

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += str(self.shunt_track_index)
        result += "$"
        result += JIKOKU_CONV.encode(self.hatsu_jikoku)
        result += "/"
        if self.chaku_jikoku:
            result += JIKOKU_CONV.encode(self.chaku_jikoku)
        result += "$"
        result += "1" if self.is_display_chaku_jikoku else "0"
        return result


@dataclass(kw_only=True)
class BeforeOperationConnect(OperationBase):
    """前作業（増結）"""

    OPERATION_TYPE: ClassVar[BOperation] = BOperation.CONNECT

    is_connect_to_front: bool
    """前方に増結するか否か"""

    connect_jikoku: Jikoku
    """増結時刻"""

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        parts = rest.split("$")
        is_connect_to_front = parts[0] == "1"
        connect_jikoku = JIKOKU_CONV.decode(parts[1])

        return cls(is_connect_to_front=is_connect_to_front, connect_jikoku=connect_jikoku)

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += "1" if self.is_connect_to_front else "0"
        result += "$"
        result += JIKOKU_CONV.encode(self.connect_jikoku)
        return result


@dataclass(kw_only=True)
class BeforeOperationRelease(OperationBase):
    """前作業（解結）"""

    OPERATION_TYPE: ClassVar[BOperation] = BOperation.RELEASE

    release_position: int
    """解結位置"""

    release_index_count: int
    """解結編成数"""

    release_jikoku: Jikoku
    """解結時刻"""

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        parts = rest.split("$")
        release_position = int(parts[0])
        release_index_count = int(parts[1].split("/")[0])
        release_jikoku = JIKOKU_CONV.decode(parts[1].split("/")[1])

        return cls(
            release_position=release_position, release_index_count=release_index_count, release_jikoku=release_jikoku
        )

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += f"{self.release_position}$"
        result += f"{self.release_index_count}/"
        result += JIKOKU_CONV.encode(self.release_jikoku)
        return result


@dataclass(kw_only=True)
class BeforeOperationOut(OperationBase):
    """前作業（出区）"""

    OPERATION_TYPE: ClassVar[BOperation] = BOperation.OUT

    out_jikoku: Jikoku
    """出区時刻"""

    in_out_link_code: str
    """入出区連携コード"""

    operation_number_original: list[str]
    """元の運用番号リスト"""

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        parts = rest.split("$")
        out_jikoku = JIKOKU_CONV.decode(parts[0])
        in_out_link_code = parts[1].split("/")[0]
        operation_number_original = parts[1].split("/")[1].split(";")

        return cls(
            out_jikoku=out_jikoku,
            in_out_link_code=in_out_link_code,
            operation_number_original=operation_number_original,
        )

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += JIKOKU_CONV.encode(self.out_jikoku)
        result += f"${self.in_out_link_code}/"
        result += ";".join(self.operation_number_original)
        return result


@dataclass(kw_only=True)
class BeforeOperationOuter(OperationBase):
    """前作業（路線外始発）"""

    OPERATION_TYPE: ClassVar[BOperation] = BOperation.OUTER

    outer_shihatsueki_index: int
    """路線外始発駅インデックス"""

    outer_shihatsu_jikoku: Jikoku
    """路線外始発時刻"""

    chaku_jikoku: Jikoku
    """着時刻"""

    in_out_link_code: str
    """入出区連携コード"""

    operation_number_original: list[str]
    """元の運用番号リスト"""

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        parts = rest.split("$")
        outer_shihatsueki_index = int(parts[0])
        outer_shihatsu_jikoku = JIKOKU_CONV.decode(parts[1].split("/")[0])
        chaku_jikoku = JIKOKU_CONV.decode(parts[1].split("/")[1])
        in_out_link_code = parts[2].split("/")[0]
        operation_number_original = parts[2].split("/")[1].split(";")

        return cls(
            outer_shihatsueki_index=outer_shihatsueki_index,
            outer_shihatsu_jikoku=outer_shihatsu_jikoku,
            chaku_jikoku=chaku_jikoku,
            in_out_link_code=in_out_link_code,
            operation_number_original=operation_number_original,
        )

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += f"{self.outer_shihatsueki_index}$"
        result += JIKOKU_CONV.encode(self.outer_shihatsu_jikoku)
        result += f"/{JIKOKU_CONV.encode(self.chaku_jikoku)}"
        result += f"${self.in_out_link_code}/"
        result += ";".join(self.operation_number_original)
        return result


@dataclass(kw_only=True)
class BeforeOperationJunction(OperationBase):
    """前作業（前列車接続）"""

    OPERATION_TYPE: ClassVar[BOperation] = BOperation.JUNCTION

    origin_jikoku: Jikoku
    """発時刻"""

    operation_number_temp: list[str]
    """一時運用番号リスト"""

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        parts = rest.split("$")
        origin_jikoku = JIKOKU_CONV.decode(parts[0])
        operation_number_temp = parts[1].split(";")

        return cls(origin_jikoku=origin_jikoku, operation_number_temp=operation_number_temp)

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += JIKOKU_CONV.encode(self.origin_jikoku)
        result += f"${';'.join(self.operation_number_temp)}"
        return result


@dataclass(kw_only=True)
class BeforeOperationNumberChange(OperationBase):
    """前作業（運用番号変更）"""

    OPERATION_TYPE: ClassVar[BOperation] = BOperation.NUMBER_CHANGE

    operation_number: list[str]
    """運用番号リスト"""

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        operation_number = list(filter(bool, rest.split(";")))

        return cls(operation_number=operation_number)

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += ";".join(self.operation_number)
        return result


class BeforeOperationFactory:
    @staticmethod
    def from_str(text: str) -> OperationBase:
        (operation_type, _) = text.split("/", 1)
        try:
            operation = BOperation(int(operation_type))
        except ValueError:
            raise ValueError(
                f"Unknown operation type: '{operation_type}', valid operation type is {', '.join([str(x.value) for x in BOperation])}"
            )

        operation_cls: Type[OperationBase] = {
            BOperation.SHUNT: BeforeOperationShunt,
            BOperation.RELEASE: BeforeOperationRelease,
            BOperation.CONNECT: BeforeOperationConnect,
            BOperation.OUT: BeforeOperationOut,
            BOperation.OUTER: BeforeOperationOuter,
            BOperation.JUNCTION: BeforeOperationJunction,
            BOperation.NUMBER_CHANGE: BeforeOperationNumberChange,
        }[operation]

        return operation_cls.from_str(text)


# endregion

# region AfterOperation


class AOperation(Enum):
    """作業種別"""

    SHUNT = 0
    """入換"""

    CONNECT = 1
    """増結"""

    RELEASE = 2
    """解結"""

    IN = 3
    """入区"""

    OUTER = 4
    """路線外終着"""

    JUNCTION = 5
    """次列車接続"""

    NUMBER_CHANGE = 6
    """運用番号変更"""


@dataclass(kw_only=True)
class AfterOperationShunt(OperationBase):
    """後作業（入換）"""

    OPERATION_TYPE: ClassVar[AOperation] = AOperation.SHUNT

    shunt_track_index: int
    """入換トラック番号"""

    hatsu_jikoku: Jikoku
    """発時刻"""

    chaku_jikoku: Jikoku
    """着時刻"""

    is_display_hatsu_jikoku: bool
    """発時刻を表示するか否か"""

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        parts = rest.split("$")
        shunt_track_index = int(parts[0])
        hatsu_jikoku = JIKOKU_CONV.decode(parts[1].split("/")[0])
        chaku_jikoku = JIKOKU_CONV.decode(parts[1].split("/")[1]) if "/" in parts[1] else Jikoku(None)
        is_display_hatsu_jikoku = parts[2] == "1"

        return cls(
            shunt_track_index=shunt_track_index,
            hatsu_jikoku=hatsu_jikoku,
            chaku_jikoku=chaku_jikoku,
            is_display_hatsu_jikoku=is_display_hatsu_jikoku,
        )

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += str(self.shunt_track_index)
        result += "$"
        result += JIKOKU_CONV.encode(self.hatsu_jikoku)
        result += "/"
        if self.chaku_jikoku:
            result += JIKOKU_CONV.encode(self.chaku_jikoku)
        result += "$"
        result += "1" if self.is_display_hatsu_jikoku else "0"
        return result


@dataclass(kw_only=True)
class AfterOperationConnect(OperationBase):
    """後作業（増結）"""

    OPERATION_TYPE: ClassVar[AOperation] = AOperation.CONNECT

    is_connect_to_front: bool
    """前方に増結するか否か"""

    connect_jikoku: Jikoku
    """増結時刻"""

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        parts = rest.split("$")
        is_connect_to_front = parts[0] == "1"
        connect_jikoku = JIKOKU_CONV.decode(parts[1])

        return cls(is_connect_to_front=is_connect_to_front, connect_jikoku=connect_jikoku)

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += "1" if self.is_connect_to_front else "0"
        result += "$"
        result += JIKOKU_CONV.encode(self.connect_jikoku)
        return result


class ReleasePosition(Enum):
    """解結編成位置"""

    AFTER = 0
    """後方の編成を解結"""

    BEFORE = 1
    """前方の編成を解結"""

    OTHER = 2
    """前方の編成以外を解結"""


@dataclass(kw_only=True)
class AfterOperationRelease(OperationBase):
    """後作業（解結）"""

    OPERATION_TYPE: ClassVar[AOperation] = AOperation.RELEASE

    release_position: ReleasePosition
    """解結編成位置"""

    release_index_count: int
    """解結編成数"""

    release_jikoku: Jikoku
    """解結時刻"""

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        parts = rest.split("$")
        release_position = ReleasePosition(int(parts[0]))
        release_index_count = int(parts[1].split("/")[0])
        release_jikoku = JIKOKU_CONV.decode(parts[1].split("/")[1])

        return cls(
            release_position=release_position, release_index_count=release_index_count, release_jikoku=release_jikoku
        )

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += f"{self.release_position.value}$"
        result += f"{self.release_index_count}/"
        result += JIKOKU_CONV.encode(self.release_jikoku)
        return result


@dataclass(kw_only=True)
class AfterOperationIn(OperationBase):
    """後作業（入区）"""

    OPERATION_TYPE: ClassVar[AOperation] = AOperation.IN

    in_jikoku: Jikoku
    """入区時刻"""

    in_out_link_code: str
    """入区リンクコード"""

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        parts = rest.split("$")
        in_jikoku = JIKOKU_CONV.decode(parts[0])
        in_out_link_code = parts[1]

        return cls(in_jikoku=in_jikoku, in_out_link_code=in_out_link_code)

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += JIKOKU_CONV.encode(self.in_jikoku)
        result += f"${self.in_out_link_code}"
        return result


@dataclass(kw_only=True)
class AfterOperationOuter(OperationBase):
    """後作業（路線外終着）"""

    OPERATION_TYPE: ClassVar[AOperation] = AOperation.OUTER

    outer_terminal_index: int
    """路線外終着駅インデックス"""

    hatsu_jikoku: Jikoku
    """発時刻"""

    outer_terminal_jikoku: Jikoku
    """路線外終着駅到着時刻"""

    in_out_link_code: str  # OuDiaSecond Ver2.05+ 入出区連携コード追加
    """入出区連携コード"""

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        parts = rest.split("$")
        outer_shuchakueki_index = int(parts[0])
        outer_shihatsu_jikoku = JIKOKU_CONV.decode(parts[1].split("/")[0])
        outer_shuchaku_jikoku = JIKOKU_CONV.decode(parts[1].split("/")[1])
        in_out_link_code = parts[2]

        return cls(
            outer_terminal_index=outer_shuchakueki_index,
            hatsu_jikoku=outer_shihatsu_jikoku,
            outer_terminal_jikoku=outer_shuchaku_jikoku,
            in_out_link_code=in_out_link_code,
        )

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += f"{self.outer_terminal_index}$"
        result += JIKOKU_CONV.encode(self.hatsu_jikoku)
        result += f"/{JIKOKU_CONV.encode(self.outer_terminal_jikoku)}"
        result += f"${self.in_out_link_code}"
        return result


@dataclass(kw_only=True)
class AfterOperationJunction(OperationBase):
    """後作業（次列車接続）"""

    # OuDiaSecond Ver2.00.05 増結表示省略設定を追加
    # OuDiaSecond Ver2.05+ 増結表示省略から次列車接続タイプに変更

    OPERATION_TYPE: ClassVar[AOperation] = AOperation.JUNCTION

    terminal_jikoku: Jikoku
    """終点時刻"""

    next_junction_type: int
    """次列車接続タイプ"""

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "next_junction_type":
            if not 0 <= value <= 3:
                raise ValueError("next_junction_type must be 0, 1, 2 or 3")
        return super().__setattr__(name, value)

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)
        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        parts = rest.split("$")
        if not len(parts) == 2:
            raise ValueError(f"{cls.__name__}: str must be split into two parts by '$'")

        terminal_jikoku = JIKOKU_CONV.decode(parts[0])
        next_junction_type = int(parts[1])

        return cls(terminal_jikoku=terminal_jikoku, next_junction_type=next_junction_type)

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += JIKOKU_CONV.encode(self.terminal_jikoku)
        result += f"${self.next_junction_type}"
        return result


@dataclass(kw_only=True)
class AfterOperationNumberChange(OperationBase):
    """後作業（運用番号変更）"""

    OPERATION_TYPE: ClassVar[AOperation] = AOperation.NUMBER_CHANGE

    operation_numbers: list[str]  # OuDiaSecond Ver2.00.05+
    """運用番号リスト"""

    @property
    def is_operation_number_reverse(self) -> bool:  # OuDiaSecond Ver2.06.05+
        """運用番号順反転の有無"""
        return not self.operation_numbers  # 運用番号が空の場合、反転が有効である

    @classmethod
    def from_str(cls, text: str) -> Self:
        operation_type, rest = text.split("/", 1)

        if operation_type != str(cls.OPERATION_TYPE.value):
            raise ValueError(f"{cls.__name__} operation type must be {cls.OPERATION_TYPE.value}")

        operation_numbers = list(filter(bool, rest.split(";")))

        return cls(operation_numbers=operation_numbers)

    def __str__(self) -> str:
        result = f"{self.OPERATION_TYPE.value}/"
        result += ";".join(self.operation_numbers)
        return result


class AfterOperationFactory:

    @classmethod
    def from_str(cls, text: str) -> OperationBase:
        operation_type, rest = text.split("/", 1)
        try:
            operation = AOperation(int(operation_type))
        except ValueError:
            raise ValueError(
                f"Unknown operation type: '{operation_type}', valid operation type is {', '.join([str(x.value) for x in AOperation])}"
            )

        operation_cls: Type[OperationBase] = {
            AOperation.SHUNT: AfterOperationShunt,
            AOperation.RELEASE: AfterOperationRelease,
            AOperation.CONNECT: AfterOperationConnect,
            AOperation.IN: AfterOperationIn,
            AOperation.OUTER: AfterOperationOuter,
            AOperation.JUNCTION: AfterOperationJunction,
            AOperation.NUMBER_CHANGE: AfterOperationNumberChange,
        }[operation]

        return operation_cls.from_str(text)


# endregion
