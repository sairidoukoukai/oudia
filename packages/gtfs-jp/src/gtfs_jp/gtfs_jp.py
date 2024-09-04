import logging
import zipfile

from gtfs_jp.stops import Stops

from dataclasses import dataclass
from io import TextIOWrapper
from os import PathLike
from typing import BinaryIO, TypeAlias

logger = logging.getLogger(__name__)

StrPath: TypeAlias = str | PathLike[str]


@dataclass
class GTFSJP:
    """GTFS-JP準拠のフォーマットの構造化形式"""

    # agency: Agency
    # """`agency.txt`: 事業者情報（必須）"""

    # agency_jp: AgencyJP | None = None
    # """`agency_jp.txt`: 事業者追加情報（任意）"""

    stops: Stops
    """`stops.txt`: 停留所・標柱情報（必須）"""

    # routes: Routes
    # """`routes.txt`: 経路情報（必須）"""

    # trips: Trips
    # """`trips.txt`: 便情報（必須）"""

    # office_jp: str | None = None
    # """`office_jp.txt`: 営業所情報（任意）"""

    # pattern_jp: str | None = None
    # """`pattern_jp.txt`: 停車パターン情報（任意）"""

    # stop_times: StopTimes
    # """`stop_times.txt`: 通過時刻情報（必須）"""

    # calendar: Calendar
    # """`calendar.txt`: 運行区分情報（条件付き必須）"""

    # calendar_dates: CalendarDates
    # """`calendar_dates.txt`: 運行日情報（条件付き必須）"""

    # fare_attributes: FareAttributes
    # """`fare_attributes.txt`: 運賃属性情報（必須）"""

    # fare_rules: FareRules
    # """`fare_rules.txt`: 運賃定義情報（条件付き必須）"""

    # shapes: Shapes
    # """`shapes.txt`: 描画情報（任意）"""

    # frequencies: Frequencies
    # """`frequencies.txt`: 運行間隔情報（任意）"""

    # transfers: Transfers
    # """`transfers.txt`: 乗換情報（任意）"""

    # feed_info: FeedInfo
    # """`feed_info.txt`: 提供情報（必須）"""

    # translations: Translations
    # """`translations.txt`: 翻訳情報（必須）"""

    @staticmethod
    def load(file: StrPath | BinaryIO) -> "GTFSJP":
        """
        GTFS-JP準拠のフォーマットを読み込み
        """
        with zipfile.ZipFile(file) as zip:
            with zip.open("stops.txt") as f:
                stops = Stops.load(TextIOWrapper(f, "utf-8-sig", newline=""))

        return GTFSJP(stops=stops)

    def save(self, file: StrPath | BinaryIO) -> None:
        """
        GTFS-JP準拠のフォーマットに保存

        Args:
            file (TextIO | str): 保存先

        Returns:
            None
        """
        if isinstance(file, str):
            if not file.endswith(".zip"):
                logger.warning("GTFS-JP data must be saved as a zip file.")

        with zipfile.ZipFile(file, "w") as zip:
            with zip.open("stops.txt", "w") as f:
                self.stops.save(TextIOWrapper(f, "utf-8-sig", newline=""))
