from collections.abc import Callable
from typing import Type, TypeVar
from gtfs_jp.stops import LocationType, Stop, Stops, WheelChairBoarding
from oudia import OuDia, Eki
from gtfs_jp import GTFSJP
from oudia import Node, TypedNode


def convert_eki_to_stop(eki: Eki, id: str) -> Stop:
    return Stop(
        stop_id=id,
        stop_code=None,
        stop_name=eki.ekimei,
        stop_desc=None,
        stop_lat=0.0,
        stop_lon=0.0,
        zone_id=None,
        stop_url=None,
        location_type=LocationType.Stop,
        parent_station=None,
        stop_timezone=None,
        wheelchair_boarding=WheelChairBoarding.Empty,
        platform_code=None,
    )


T = TypeVar("T", bound=TypedNode)


def find_all_nodes_of_type(current: OuDia | TypedNode | Node, node: Type[T]) -> list[T]:
    result: list[T] = []

    if isinstance(current, node):
        result.append(current)

    for c in current.children:
        result.extend(find_all_nodes_of_type(c, node))

    return result


def convert_oudia_to_gtfs(
    oudia: OuDia,
    generate_stop_id: Callable[[int, Eki], str] = lambda i, eki: f"{i}",
) -> GTFSJP:
    ekis = find_all_nodes_of_type(oudia, Eki)

    print(ekis)
    stops = [convert_eki_to_stop(eki, generate_stop_id(i, eki)) for i, eki in enumerate(ekis)]
    return GTFSJP(stops=Stops(stops))
