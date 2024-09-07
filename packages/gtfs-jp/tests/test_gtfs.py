from gtfs_jp import GTFSJP, Stops, Stop, LocationType, WheelChairBoarding

M01 = Stop(
    stop_id="mk_1_1",
    stop_code="M01",
    stop_name="再履駅",
    stop_desc=None,
    stop_lat=34.805429,
    stop_lon=135.455365,
    zone_id=None,
    stop_url="http://example.com",
    location_type=LocationType.Stop,
    parent_station=None,
    stop_timezone=None,
    wheelchair_boarding=WheelChairBoarding.Empty,
    platform_code=None,
)

M02 = Stop(
    stop_id="mk_1_2",
    stop_code="M02",
    stop_name="バス駅",
    stop_desc=None,
    stop_lat=34.805429,
    stop_lon=135.455365,
    zone_id=None,
    stop_url="http://example.com",
    location_type=LocationType.Stop,
    parent_station=None,
    stop_timezone=None,
    wheelchair_boarding=WheelChairBoarding.Empty,
    platform_code=None,
)


def test_stops():

    stops = Stops([M01, M02])

    GTFSJP(stops=stops).save("gtfs_jp.zip")

    gtfs = GTFSJP.load("gtfs_jp.zip")

    assert gtfs.stops == stops

    for stop in gtfs.stops:
        print(stop.stop_id, stop.stop_name, stop.stop_lat, stop.stop_lon)
