from dataclasses import dataclass
from enum import Enum

from oudia.dia.jikoku import Hour, Jikoku, JikokuConv, Second

JIKOKU_CONV = JikokuConv(True, hour=Hour.ZERO_TO_NONE, second=Second.NOT_IF_ZERO)


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


@dataclass
class BeforeOperation:
    """前作業"""

    # TODO: Use meaningful fields instead of dummy values, make a class for each operation type

    operation: BOperation

    bool_data_1: bool
    bool_data_2: bool

    int_data_1: int
    int_data_2: int
    int_data_3: int

    jikoku_data_1: Jikoku
    jikoku_data_2: Jikoku
    jikoku_data_3: Jikoku

    operation_number_1: list[str]
    operation_number_2: list[str]
    operation_number_3: list[str]

    in_out_link_code: str

    before_operation_list: list["BeforeOperation"]
    after_operation_list: list["AfterOperation"]

    @classmethod
    def from_str(cls, text: str) -> "BeforeOperation":
        # TODO:
        return cls(
            operation=BOperation(int(text[0])),
            bool_data_1=False,
            bool_data_2=False,
            int_data_1=0,
            int_data_2=0,
            int_data_3=0,
            jikoku_data_1=Jikoku(None),
            jikoku_data_2=Jikoku(None),
            jikoku_data_3=Jikoku(None),
            operation_number_1=[],
            operation_number_2=[],
            operation_number_3=[],
            in_out_link_code="",
            before_operation_list=[],
            after_operation_list=[],
        )

    def __str__(self) -> str:
        result = f"{self.operation.value}/"
        match self.operation:
            case BOperation.SHUNT:
                result += str(self.int_data_1)  # shuntTrackIndex
                result += "$"
                result += JIKOKU_CONV.encode(self.jikoku_data_1)  # hastuJikoku
                result += "/"
                if self.jikoku_data_2:
                    result += JIKOKU_CONV.encode(self.jikoku_data_2)  # chakuJikoku
                result += "$"
                result += "1" if self.bool_data_1 else "0"  # isDisplayChakuJikoku

            case BOperation.CONNECT:
                result += "1" if self.bool_data_1 else "0"  # IsConnectToFront
                result += "$"
                result += JIKOKU_CONV.encode(self.jikoku_data_1)  # Connect Jikoku

                # TODO: Child operations here

            case BOperation.RELEASE:
                result += str(self.int_data_1)  # Release Position
                result += "$"
                result += str(self.int_data_2)  # Release Index Count
                result += "/"
                result += JIKOKU_CONV.encode(self.jikoku_data_1)  # Release Jikoku
                # TODO: Child operations here

            case BOperation.OUT:
                result += JIKOKU_CONV.encode(self.jikoku_data_1)  # Out Jikoku
                result += "$"
                result += self.in_out_link_code  # InOutLinkCode
                result += "/"
                result += ";".join(self.operation_number_1)  # Operation Number Original (joined with ;)

            case BOperation.OUTER:
                result += str(self.int_data_1)  # Outer Shihatsueki Index
                result += "$"
                result += JIKOKU_CONV.encode(self.jikoku_data_1)  # Outer Shihatsu Jikoku
                result += "/"
                result += JIKOKU_CONV.encode(self.jikoku_data_2)  # Chaku Jikoku
                result += "$"
                result += self.in_out_link_code  # InOutLinkCode
                result += "/"
                result += ";".join(self.operation_number_1)  # Operation Number Original (joined with ;)

            case BOperation.JUNCTION:
                result += JIKOKU_CONV.encode(self.jikoku_data_1)  # Origin Jikoku
                result += "$"
                result += ";".join(self.operation_number_1)  # Operation Number Temp (joined with ;)

            case BOperation.NUMBER_CHANGE:
                result += ";".join(self.operation_number_1)  # Operation Number (joined with ;)
                if not self.bool_data_1:  # Operation Number Reverse is False
                    result += ""

        return result


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


@dataclass
class AfterOperation:
    """後作業"""

    operation: AOperation

    bool_data_1: bool
    bool_data_2: bool

    int_data_1: int
    int_data_2: int

    jikoku_data_1: Jikoku
    jikoku_data_2: Jikoku

    operation_number_1: list[str]
    operation_number_2: list[str]
    operation_number_3: list[str]

    in_out_link_code: str

    before_operation_list: list["BeforeOperation"]
    after_operation_list: list["AfterOperation"]

    @classmethod
    def from_str(cls, text: str) -> "AfterOperation":
        # TODO:
        return cls(
            operation=AOperation(int(text[0])),
            bool_data_1=False,
            bool_data_2=False,
            int_data_1=0,
            int_data_2=0,
            jikoku_data_1=Jikoku(None),
            jikoku_data_2=Jikoku(None),
            operation_number_1=[],
            operation_number_2=[],
            operation_number_3=[],
            in_out_link_code="",
            before_operation_list=[],
            after_operation_list=[],
        )

    def __str__(self) -> str:
        result = f"{self.operation.value}/"

        match self.operation:
            case AOperation.SHUNT:
                result += str(self.int_data_1)  # shuntTrackIndex
                result += "$"
                result += JIKOKU_CONV.encode(self.jikoku_data_1)  # Operation Hatsu Jikoku
                result += "/"
                if self.jikoku_data_2:  # Operation Chaku Jikoku (if not null)
                    result += JIKOKU_CONV.encode(self.jikoku_data_2)
                result += "$"
                result += "1" if self.bool_data_1 else "0"  # isDisplayHatsuJikoku

            case AOperation.CONNECT:
                result += "1" if self.bool_data_1 else "0"  # IsConnectToFront
                result += "$"
                result += JIKOKU_CONV.encode(self.jikoku_data_1)  # Connect Jikoku

            case AOperation.RELEASE:
                result += str(self.int_data_1)  # Release Position
                result += "$"
                result += str(self.int_data_2)  # Release Index Count
                result += "/"
                result += JIKOKU_CONV.encode(self.jikoku_data_1)  # Release Jikoku

            case AOperation.IN:
                result += JIKOKU_CONV.encode(self.jikoku_data_1)  # In Jikoku
                result += "$"
                result += self.in_out_link_code  # InOutLinkCode

            case AOperation.OUTER:
                result += str(self.int_data_1)  # Outer Shuchakueki Index
                result += "$"
                result += JIKOKU_CONV.encode(self.jikoku_data_1)  # Hatsu Jikoku
                result += "/"
                result += JIKOKU_CONV.encode(self.jikoku_data_2)  # Outer Shuchaku Jikoku
                result += "$"
                result += self.in_out_link_code  # InOutLinkCode

            case AOperation.JUNCTION:
                result += JIKOKU_CONV.encode(self.jikoku_data_1)  # Terminal Jikoku
                result += "$"
                result += str(self.int_data_1)  # Next Junction Type

            case AOperation.NUMBER_CHANGE:
                if not self.bool_data_1:  # Operation Number Reverse is False
                    result += ";".join(self.operation_number_1)  # Operation Number (joined with ;)

        return result
