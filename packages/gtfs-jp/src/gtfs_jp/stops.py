from csv import DictReader
from dataclasses import dataclass
from enum import Enum
from io import TextIOBase

from gtfs_jp.record import Record, RecordsFile


class LocationType(Enum):
    """停留所・標柱区分"""

    Stop = 0
    Station = 1
    # Entrance/Exit = 2
    # Generic Node = 3
    # Boarding Area = 4


class WheelChairBoarding(Enum):
    """車椅子情報"""

    Empty = 0
    Some = 1
    No = 2


@dataclass
class Stop(Record):
    """停留所・標柱"""

    stop_id: str
    """停留所・標柱ID（必須）"""

    stop_code: str | None
    """停留所・標柱番号（任意）"""

    stop_name: str
    """停留所・標柱名称（必須）"""

    stop_desc: str | None
    """停留所・標柱付加情報（任意）"""

    stop_lat: float
    """緯度（必須）"""

    stop_lon: float
    """経度（必須）"""

    zone_id: str | None
    """運賃エリアID（任意）"""

    stop_url: str
    """停留所・標柱URL（必須）"""

    location_type: LocationType
    """停留所・標柱区分（必須）"""

    parent_station: str | None
    """親停留所情報（任意）"""

    stop_timezone: str | None
    """タイムゾーン（不要）"""

    wheelchair_boarding: WheelChairBoarding
    """車椅子情報（不要）"""

    platform_code: str | None
    """のりば情報（任意）"""

    @staticmethod
    def from_dict(record: dict[str, str]) -> "Stop":
        return Stop(
            stop_id=record["stop_id"],
            stop_code=Record.parse_text_value(record.get("stop_code")),
            stop_name=record["stop_name"],
            stop_desc=Record.parse_text_value(record.get("stop_desc")),
            stop_lat=float(record["stop_lat"]),
            stop_lon=float(record["stop_lon"]),
            zone_id=Record.parse_text_value(record.get("zone_id")),
            stop_url=record["stop_url"],
            location_type=(
                LocationType(int(location_type))
                if (location_type := record.get("location_type"))
                else LocationType.Stop
            ),
            parent_station=Record.parse_text_value(record.get("parent_station")),
            stop_timezone=Record.parse_text_value(record.get("stop_timezone")),
            wheelchair_boarding=(
                WheelChairBoarding(int(wheelchair_boarding))
                if (wheelchair_boarding := record.get("wheelchair_boarding"))
                else WheelChairBoarding.Empty
            ),
            platform_code=Record.parse_text_value(record.get("platform_code")),
        )


@dataclass
class Stops(RecordsFile[Stop]):
    pass

    @staticmethod
    def load(file: TextIOBase) -> "Stops":
        reader = DictReader(file)
        records = [Stop.from_dict(record) for record in reader]
        return Stops(records)
