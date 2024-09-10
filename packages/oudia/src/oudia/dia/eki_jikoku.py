from dataclasses import dataclass
from enum import Enum
from typing import Self

from oudia.dia.jikoku import Hour, Jikoku, JikokuConv, Second
from oudia.dia.operation import OperationBase

JIKOKU_CONV = JikokuConv(no_colon=True, hour=Hour.ZERO_TO_NONE, second=Second.NOT_IF_ZERO)


class Ekiatsukai(Enum):
    """駅扱"""

    NONE = 0
    """なし"""

    TEISYA = 1
    """停車"""

    TSUUKA = 2
    """通過"""


@dataclass(kw_only=True)
class EkiJikoku:
    """駅時刻"""

    ekiatsukai: Ekiatsukai
    """駅扱"""

    chaku_jikoku: Jikoku
    """着時刻"""

    hatsu_jikoku: Jikoku
    """発時刻"""

    ressya_track_index: int | None
    """列車の番線"""

    before_operation_list: list[OperationBase]
    """前作業"""

    after_operation_list: list[OperationBase]
    """後作業"""

    def __str__(self) -> str:
        result = ""
        result += str(self.ekiatsukai.value)

        chaku_jikoku = JIKOKU_CONV.encode(self.chaku_jikoku, True, None)
        hatsu_jikoku = JIKOKU_CONV.encode(self.hatsu_jikoku, False, None)

        if chaku_jikoku or hatsu_jikoku:
            result += ";"

            if chaku_jikoku:
                result += chaku_jikoku
                result += "/"

            result += hatsu_jikoku

        if self.ressya_track_index is not None:
            result += "$" + str(self.ressya_track_index)

        return result

    @classmethod
    def from_str(cls, text: str) -> Self:
        ekiatsukai = Ekiatsukai(int(text[0]))

        chaku_time = None
        hatsu_time = None
        ressya_track_index = None

        if len(text) >= 3:
            if text[1] == ";":
                rest_part = text[2:]

                if "$" in rest_part:
                    time, ressya_track = rest_part.split("$", 1)
                    ressya_track_index = int(ressya_track)
                else:
                    time = rest_part

                if "/" in time:
                    chaku_time, hatsu_time = time.split("/", 1)
                else:
                    chaku_time = None
                    hatsu_time = time
            elif text[1] == "$":
                chaku_time = None
                hatsu_time = None
                ressya_track_index = int(text[2:])
            else:
                raise ValueError(f"Invalid text: {text}")

        chaku_jikoku = JIKOKU_CONV.decode(chaku_time) if chaku_time else Jikoku(None)
        hatsu_jikoku = JIKOKU_CONV.decode(hatsu_time) if hatsu_time else Jikoku(None)

        return cls(
            ekiatsukai=ekiatsukai,
            chaku_jikoku=chaku_jikoku,
            hatsu_jikoku=hatsu_jikoku,
            ressya_track_index=ressya_track_index,
            before_operation_list=[],
            after_operation_list=[],
        )
