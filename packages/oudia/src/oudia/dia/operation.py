from enum import Enum

from oudia.dia.jikoku import Jikoku


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


class BeforeOperation:
    """前作業"""

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
