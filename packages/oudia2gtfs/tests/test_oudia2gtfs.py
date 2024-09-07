# # from oudia2gtfs import


# def test_hello():
#     return hello()


from gtfs_jp.gtfs_jp import GTFSJP
from gtfs_jp.stops import LocationType, Stop, Stops, WheelChairBoarding
import oudia
from oudia2gtfs import convert_oudia_to_gtfs


# def test_convert():
#     dia = oudia.loads(
#         "FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\nEki.\nEkimei=再履駅\nEkijikokukeisiki=Jikokukeisiki_NoboriChaku\nEkikibo=Ekikibo_Ippan\n.\nEki.\nEkimei=バス駅\nEkijikokukeisiki=Jikokukeisiki_NoboriChaku\nEkikibo=Ekikibo_Ippan\n.\n.\n.\nAfterMath=Hello"
#     )

#     assert convert_oudia_to_gtfs(dia) == GTFSJP(
#         stops=Stops(
#             records=[
#                 Stop(
#                     stop_id="0",
#                     stop_code=None,
#                     stop_name="再履駅",
#                     stop_desc=None,
#                     stop_lat=0.0,
#                     stop_lon=0.0,
#                     zone_id=None,
#                     stop_url=None,
#                     location_type=LocationType.Stop,
#                     parent_station=None,
#                     stop_timezone=None,
#                     wheelchair_boarding=WheelChairBoarding.Empty,
#                     platform_code=None,
#                 ),
#                 Stop(
#                     stop_id="1",
#                     stop_code=None,
#                     stop_name="バス駅",
#                     stop_desc=None,
#                     stop_lat=0.0,
#                     stop_lon=0.0,
#                     zone_id=None,
#                     stop_url=None,
#                     location_type=LocationType.Stop,
#                     parent_station=None,
#                     stop_timezone=None,
#                     wheelchair_boarding=WheelChairBoarding.Empty,
#                     platform_code=None,
#                 ),
#             ]
#         )
#     )

#     gtfs = convert_oudia_to_gtfs(dia)
#     gtfs.save("gtfs_from_oudia.zip")
