from typing import TypedDict


class Stop(TypedDict):
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
    """運賃エリアID（条件付き必須）"""

    stop_url: str | None
    """停留所・標柱URL（任意）"""

    location_type: int
    """停留所・標柱区分（任意）"""

    parent_station: str | None
    """親停留所情報（任意）"""

    stop_timezone: str | None
    """タイムゾーン（不要）"""

    wheelchair_boarding: int
    """車椅子情報（不要）"""

    platform_code: str | None
    """のりば情報（任意）"""


class Route(TypedDict):
    route_id: str
    """路線ID（必須）"""

    route_short_name: str
    """路線短縮名（必須）"""

    route_long_name: str
    """路線長縮名（必須）"""

    route_desc: str | None
    """路線説明（任意）"""

    route_type: int
    """路線区分（必須）"""

    route_url: str | None
    """路線URL（任意）"""

    route_color: str | None
    """路線色（任意）"""

    route_text_color: str | None
    """路線色（任意）"""

    route_sort_order: int
    """路線表示順序（必須）"""


class Trip(TypedDict):
    route_id: str
    """経路ID（必須）"""

    service_id: str
    """運行日ID（必須）"""

    trip_id: str
    """便ID（必須）"""

    trip_headsign: str | None
    """便行先（任意）"""

    trip_short_name: str | None
    """便名（任意）"""

    direction_id: int
    """往復区分（任意）
    
    - 0: 復路（上り）
    - 1: 往路（下り）
    """

    block_id: str | None
    """便結合区分（任意）"""

    shape_id: str | None
    """描画ID（任意）"""

    wheelchair_accessible: int
    """車いす利用区分（任意）"""

    bikes_allowed: int
    """自転車持込区分（任意）"""

    jp_trip_desc: str | None
    """便情報（任意）"""

    jp_trip_desc_symbol: str | None
    """便記号（任意）"""

    jp_office_id: str | None
    """営業所ID（任意）"""

    jp_pattern_id: str | None
    """停車パターンID（任意）"""


class StopTime(TypedDict):
    trip_id: str
    """便ID（必須）"""

    arrival_time: str
    """到着時刻（必須）"""

    departure_time: str
    """出発時刻（必須）"""

    stop_id: str
    """標柱ID（必須）"""

    stop_sequence: int
    """通過順位（必須）"""

    stop_headsign: str
    """停留所行先（任意）"""

    pickup_type: int
    """乗車区分（任意）"""

    drop_off_type: int
    """降車区分（任意）"""

    shape_dist_traveled: int
    """通算距離（任意）"""
