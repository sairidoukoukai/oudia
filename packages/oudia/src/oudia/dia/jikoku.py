from dataclasses import dataclass
from enum import Enum
from typing import Self

MINUTES_AN_HOUR = 60
SECONDS_AN_MINUTE = 60
HOURS_A_DAY = 24

SECONDS_A_DAY = SECONDS_AN_MINUTE * MINUTES_AN_HOUR * HOURS_A_DAY


@dataclass
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
