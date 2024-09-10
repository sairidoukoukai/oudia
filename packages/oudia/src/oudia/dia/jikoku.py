from dataclasses import dataclass
from enum import Enum
from typing import Self

MINUTES_AN_HOUR = 60
SECONDS_AN_MINUTE = 60
HOURS_A_DAY = 24

SECONDS_A_DAY = SECONDS_AN_MINUTE * MINUTES_AN_HOUR * HOURS_A_DAY


@dataclass(kw_only=True)
class Jikoku:
    """時刻"""

    __total_seconds: int | None = None
    """総秒数"""

    def __init__(self, total_seconds: int | None = None):
        """
        秒単位の時刻を作成します。

        引数:
            total_seconds (int | None): 00:00から経過した総秒数で、24:00以上の場合は0に戻り、00:00以下の場合は24:00から減算した秒数になる。
        """
        self.total_seconds = total_seconds

    @property
    def total_seconds(self) -> int | None:
        """総秒数"""
        return self.__total_seconds

    @total_seconds.setter
    def total_seconds(self, value: int | None) -> None:
        self.__total_seconds = value % SECONDS_A_DAY if value is not None else None

    def get_hour(self) -> int:
        """経過秒数から時を取得"""
        return self.total_seconds // 3600 if self.total_seconds else 0

    def get_minute(self) -> int:
        """経過秒数から分を取得"""
        return ((self.total_seconds % 3600) // 60) if self.total_seconds else 0

    def get_second(self) -> int:
        """経過秒数から秒を取得"""
        return (self.total_seconds % 60) if self.total_seconds else 0

    def set_time(self, hour: int, minute: int, second: int = 0) -> Self:
        """時・分・秒を指定して時刻を設定

        引数:
            hour (int): 時（0以上24未満）
            minute (int): 分（0以上60未満）
            second (int): 秒（0以上60未満）
        """
        self.total_seconds = hour * 3600 + minute * 60 + second
        return self

    def add_seconds(self, value: int):
        """現在の時刻に秒数を加算

        引数:
            value (int): 加算する秒数
        """
        if self.total_seconds is not None:
            self.total_seconds += value
        return self

    def compare(self, other: Self) -> int:
        """時刻を比較

        引数:
            other (Jikoku): 比較対象
        """
        if self.total_seconds is None and other.total_seconds is None:
            return 0
        if self.total_seconds is None:
            return -1
        if other.total_seconds is None:
            return 1
        match self.total_seconds - other.total_seconds:
            case x if x > 0:
                return 1
            case x if x < 0:
                return -1
            case _:
                return 0

    def __eq__(self, other: Self) -> bool:
        return self.compare(other) == 0

    def __lt__(self, other: Self) -> bool:
        return self.compare(other) == -1

    def __gt__(self, other: Self) -> bool:
        return self.compare(other) == 1

    def __bool__(self) -> bool:
        return self.total_seconds is not None

    def __str__(self):
        return f"{self.get_hour():02}:{self.get_minute():02}:{self.get_second():02}" if self else ""


class Hour(Enum):
    """時の変換方法"""

    ZERO = 0
    """'0X' -> '0X'"""

    ZERO_TO_NONE = 1
    """'0X' -> 'X'"""

    ZERO_TO_SPACE = 2
    """'0X' -> ' X'"""


class Second(Enum):
    """秒の変換方法"""

    OUTPUT = 0
    """秒を出力"""

    NO_SECOND = 1
    """秒を出力しない"""

    NOT_IF_ZERO = 2
    """秒が0の場合は出力しない"""


class SecondRound(Enum):
    ROUND_DOWN = 0
    """切り捨て"""

    ROUND = 1
    """30秒で四捨五入"""

    ROUND_UP = 2
    """切り上げ"""


@dataclass(kw_only=True)
class JikokuConv:
    """時刻の変換"""

    no_colon: bool = False
    """コロンの有無"""

    hour: Hour = Hour.ZERO
    """時の変換方法"""

    second: Second = Second.OUTPUT
    """秒の変換方法"""

    second_round_chaku: SecondRound = SecondRound.ROUND_DOWN
    """秒の丸め方（着）"""

    second_round_hatsu: SecondRound = SecondRound.ROUND_DOWN
    """秒の丸め方（発）"""

    display_2400: bool = False
    """24:00以上を表示"""

    def encode(
        self,
        jikoku: Jikoku,
        is_chaku_jikoku: bool = False,
        compare_jikoku: Jikoku | None = None,
    ) -> str:
        if not jikoku:
            return ""

        temp_jikoku = Jikoku(jikoku.total_seconds)

        if self.second == Second.NO_SECOND:
            if not compare_jikoku:
                if (is_chaku_jikoku and self.second_round_chaku == SecondRound.ROUND_UP) or (
                    not is_chaku_jikoku and self.second_round_hatsu == SecondRound.ROUND_UP
                ):
                    temp_jikoku.add_seconds(59)
                elif (is_chaku_jikoku and self.second_round_chaku == SecondRound.ROUND) or (
                    not is_chaku_jikoku and self.second_round_hatsu == SecondRound.ROUND
                ):
                    temp_jikoku.add_seconds(30)
            else:
                if (
                    jikoku.get_hour() == compare_jikoku.get_hour()
                    and jikoku.get_minute() == compare_jikoku.get_minute()
                ):
                    if (
                        is_chaku_jikoku
                        and self.second_round_chaku == SecondRound.ROUND_UP
                        and jikoku.get_second() > 0
                        and jikoku.get_second() < 30
                        and compare_jikoku.get_second() > 0
                        and compare_jikoku.get_second() < 30
                    ):
                        pass  # Skip rounding
                    elif (
                        not is_chaku_jikoku
                        and self.second_round_hatsu == SecondRound.ROUND_DOWN
                        and jikoku.get_second() >= 30
                        and compare_jikoku.get_second() >= 30
                    ):
                        temp_jikoku.add_seconds(59)
                    elif (
                        is_chaku_jikoku
                        and self.second_round_chaku == SecondRound.ROUND_UP
                        and jikoku.get_second() < 30
                        and compare_jikoku.get_second() >= 30
                    ):
                        if jikoku.get_second() + compare_jikoku.get_second() >= 60:
                            temp_jikoku.add_seconds(59)
                else:
                    if (is_chaku_jikoku and self.second_round_chaku == SecondRound.ROUND_UP) or (
                        not is_chaku_jikoku and self.second_round_hatsu == SecondRound.ROUND_UP
                    ):
                        temp_jikoku.add_seconds(59)
                    elif (is_chaku_jikoku and self.second_round_chaku == SecondRound.ROUND) or (
                        not is_chaku_jikoku and self.second_round_hatsu == SecondRound.ROUND
                    ):
                        temp_jikoku.add_seconds(30)

        hour = temp_jikoku.get_hour()
        if self.display_2400 and is_chaku_jikoku and hour == 0 and temp_jikoku.get_minute() == 0:
            hour = 24

        if self.hour == Hour.ZERO_TO_NONE:
            hour_str = f"{hour}"
        elif self.hour == Hour.ZERO_TO_SPACE:
            hour_str = f"{hour:2}"
        else:
            hour_str = f"{hour:02}"

        if not self.no_colon:
            hour_str += ":"

        minute_str = f"{temp_jikoku.get_minute():02}"

        result = hour_str + minute_str

        if self.second == Second.OUTPUT or (self.second == Second.NOT_IF_ZERO and temp_jikoku.get_second() != 0):
            if not self.no_colon:
                result += ":"
            result += f"{temp_jikoku.get_second():02}"

        return result

    def decode(
        self,
        time_str: str,
        is_chaku_jikoku: bool = False,
    ) -> Jikoku:
        if not time_str:
            return Jikoku(None)

        time_str = time_str.strip()

        if self.hour is Hour.ZERO_TO_NONE or self.hour is Hour.ZERO_TO_SPACE:
            if len(time_str) == 3 or len(time_str) == 5:
                time_str = "0" + time_str

        if self.no_colon:
            if len(time_str) == 4 or len(time_str) == 3:
                hour_str = time_str[:2]
                minute_str = time_str[2:]
                second_str = None
            elif len(time_str) == 6 or len(time_str) == 5:
                hour_str = time_str[:2]
                minute_str = time_str[2:4]
                second_str = time_str[4:]
            else:
                raise ValueError(f"Invalid time format: {time_str}")
        else:
            time_parts = time_str.split(":")
            if len(time_parts) == 2:
                hour_str, minute_str = time_parts
                second_str = None
            elif len(time_parts) == 3:
                hour_str, minute_str, second_str = time_parts
            else:
                raise ValueError(f"Invalid time format: {time_str}")

        if self.display_2400 and is_chaku_jikoku and hour_str == "24" and minute_str == "00":
            hour = 0
            minute = 0
            second = 0
        else:
            hour = int(hour_str)
            minute = int(minute_str)
            second = int(second_str) if second_str else 0

        total_seconds = hour * 3600 + minute * 60 + second

        if minute > 59:
            raise ValueError("Invalid minute value")

        if second > 59:
            raise ValueError("Invalid second value")

        if self.second == Second.NO_SECOND:
            # Reverse rounding behavior (if it was rounded during encode)
            if self.second_round_chaku == SecondRound.ROUND_UP and is_chaku_jikoku:
                total_seconds = max(total_seconds - 59, 0)
            elif self.second_round_hatsu == SecondRound.ROUND_UP and not is_chaku_jikoku:
                total_seconds = max(total_seconds - 59, 0)
            elif self.second_round_chaku == SecondRound.ROUND and is_chaku_jikoku:
                total_seconds = max(total_seconds - 30, 0)
            elif self.second_round_hatsu == SecondRound.ROUND and not is_chaku_jikoku:
                total_seconds = max(total_seconds - 30, 0)

        return Jikoku(total_seconds)
