from os import PathLike
from typing import TypeAlias, cast

import numpy as np
from oudia.nodes.ressya import Ressya
from .gtfs import Stop, Route, StopTime, Trip

from oudia import OuDia, Eki


import egGTFS
from oudia.nodes.crossing_check_rule import CrossingCheckRule
from oudia.nodes.dia import Dia, Kudari, Nobori
from oudia.nodes.disp_prop import DispProp, FontProperty
from oudia.nodes.eki import Ekijikokukeisiki
from oudia.nodes.node import NodeList
from oudia.nodes.outer_terminal import OuterTerminal
from oudia.nodes.ressyasyubetsu import Ressyasyubetsu
from oudia.nodes.rosen import Rosen
from oudia.nodes.track import EkiTrack2
from oudia.nodes.window_placement import WindowPlacement
import pandas as pd


DEFAULT_DISP_PROP_OUD2 = DispProp(
    jikokuhyou_font=[
        FontProperty(point_text_height=10, facename="Meiryo UI"),
        FontProperty(point_text_height=10, facename="Meiryo UI", bold=True),
        FontProperty(point_text_height=10, facename="Meiryo UI", itaric=True),
        FontProperty(point_text_height=10, facename="Meiryo UI"),
        FontProperty(point_text_height=10, facename="Meiryo UI"),
        FontProperty(point_text_height=10, facename="Meiryo UI"),
        FontProperty(point_text_height=10, facename="Meiryo UI"),
        FontProperty(point_text_height=10, facename="Meiryo UI", bold=True, itaric=True),
    ],
    jikokuhyou_v_font=FontProperty.from_str("PointTextHeight=9;Facename=@メイリオ"),
    dia_ekimei_font=FontProperty.from_str("PointTextHeight=9;Facename=Meiryo UI"),
    dia_jikoku_font=FontProperty.from_str("PointTextHeight=9;Facename=Meiryo UI"),
    dia_ressya_font=FontProperty.from_str("PointTextHeight=9;Facename=Meiryo UI"),
    operation_table_font=FontProperty.from_str("PointTextHeight=9;Facename=Meiryo UI"),
    all_operation_table_jikoku_font=FontProperty.from_str("PointTextHeight=8;Facename=Meiryo UI"),
    comment_font=FontProperty.from_str("PointTextHeight=9;Facename=Meiryo UI"),
    dia_moji_color="00000000",
    dia_back_color=["00FFFFFF", "00FFFFFF", "00FFFFFF", "00FFFFFF", "00FFFFFF"],
    dia_haikei_color=[],
    dia_ressya_color="00000000",
    dia_jiku_color="00C0C0C0",
    jikokuhyou_back_color=["00FFFFFF", "00F0F0F0", "00FFFFFF", "00FFFFFF"],
    std_ope_time_lower_color="00E0E0FF",
    std_ope_time_higher_color="00FFFFE0",
    std_ope_time_undef_color="0080FFFF",
    std_ope_time_illegal_color="00A0A0A0",
    operation_string_color="00000000",
    operation_grid_color="00000000",
    ekimei_length=6,
    jikokuhyou_ressya_width=5,
    any_second_inc_dec1=5,
    any_second_inc_dec2=15,
    display_ressyamei=True,
    display_outer_terminal_ekimei_origin_side=False,
    display_outer_terminal_ekimei_terminal_side=False,
    diagram_display_outer_terminal=0,
    second_round_chaku=0,
    second_round_hatsu=0,
    display_2400=False,
    operation_number_rows=1,
    display_in_out_link_code=False,
)

DEFAULT_WINDOW_PLACEMENT_OUD2 = WindowPlacement(
    rosen_view_width=263,
)


def convert_stop_to_eki(stop: Stop, first: bool = False) -> Eki:
    return Eki(
        ekimei=stop["stop_name"],
        ekikibo="Ekikibo_Ippan",
        ekijikokukeisiki=Ekijikokukeisiki.NOBORI_CHAKU if first else Ekijikokukeisiki.HATSU,
        eki_tracks=NodeList(
            EkiTrack2,
            [
                EkiTrack2(
                    track_name="1番線",
                    track_ryakusyou="1",
                ),
                EkiTrack2(
                    track_name="2番線",
                    track_ryakusyou="2",
                ),
            ],
        ),
        down_main=0,
        up_main=1,
        outer_terminals=NodeList(OuterTerminal, []),
        jikokuhyou_jikoku_display_kudari="0,1",
        jikokuhyou_jikoku_display_nobori="1,0",
        jikokuhyou_syubetsu_change_display_kudari="0,0,0,0,1",
        jikokuhyou_syubetsu_change_display_nobori="0,0,0,0,1",
        diagram_color_next_eki=0,
        jikokuhyou_outer_display_kudari="0,0",
        jikokuhyou_outer_display_nobori="0,0",
        crossing_check_rule_list=NodeList(CrossingCheckRule, []),
    )


from oudia.dia.eki_jikoku import EkiJikoku, Ekiatsukai
from oudia.dia.jikoku import Jikoku, JikokuConv, Hour, Second, SecondRound

JIKOKU_CONV = JikokuConv(
    no_colon=False,
    hour=Hour.ZERO,
    second=Second.OUTPUT,
)

StrPath: TypeAlias = str | PathLike[str]


class RouteConverter:
    route: Route
    gtfs: egGTFS.egGTFS

    trips: pd.DataFrame
    """Trips in Route"""

    stops: pd.DataFrame
    """Stop times in Route"""

    calendars: pd.DataFrame
    stop_times: pd.DataFrame

    sorted_stops: list[Stop]

    def __init__(self, gtfs: egGTFS.egGTFS, route: dict) -> None:
        self.route = cast(Route, route)
        self.gtfs = gtfs

        if self.gtfs.trips.df is None:
            raise ValueError("no trips")
        if self.gtfs.stops.df is None:
            raise ValueError("no stops")
        if self.gtfs.calendar.df is None:
            raise ValueError("no calendar")
        if self.gtfs.trips.df is None:
            raise ValueError("no trips")
        if self.gtfs.stop_times.df is None:
            raise ValueError("no stop_times")

        self.trips = self.gtfs.trips.df[self.gtfs.trips.df["route_id"] == self.route["route_id"]]
        self.stop_times = self.gtfs.stop_times.df[self.gtfs.stop_times.df["trip_id"].isin(self.trips["trip_id"])]
        self.stops = self.gtfs.stops.df[self.gtfs.stops.df["stop_id"].isin(self.stop_times["stop_id"])]
        self.calendars = self.gtfs.calendar.df[self.gtfs.calendar.df["service_id"].isin(self.trips["service_id"])]

    @property
    def route_id(self) -> str:
        return self.route["route_id"]

    @property
    def route_short_name(self) -> str:
        return self.route["route_short_name"]

    @property
    def route_long_name(self) -> str:
        return self.route["route_long_name"]

    @staticmethod
    def convert_stop_time_to_ekijikoku(stop_time: dict) -> EkiJikoku:
        return EkiJikoku(
            ekiatsukai=Ekiatsukai.TEISYA,
            chaku_jikoku=JIKOKU_CONV.decode(stop_time["arrival_time"]),
            hatsu_jikoku=JIKOKU_CONV.decode(stop_time["departure_time"]),
            ressya_track_index=1,
            before_operation_list=[],
            after_operation_list=[],
        )

    def convert_trip_to_ressya(self, trip: Trip) -> Ressya:
        if self.gtfs.stop_times.df is None:
            raise ValueError("no stop_times")

        stop_times = self.gtfs.stop_times.df[self.gtfs.stop_times.df["trip_id"] == trip["trip_id"]]

        stop_id_2_stop_time: dict[str, StopTime] = {
            stop_time["stop_id"]: cast(StopTime, stop_time) for stop_time in stop_times.to_dict(orient="records")
        }

        eki_jikoku_list = []

        stop_dict = self.sorted_stops

        if trip["direction_id"] == 0:
            stop_dict = list(reversed(stop_dict))

        for stop in stop_dict:
            stop_id = cast(Stop, stop)["stop_id"]

            stop_times_found = []
            for stop_time in stop_id_2_stop_time.values():
                if stop_id == stop_time["stop_id"]:
                    stop_times_found.append(stop_time)
            if stop_times_found:
                eki_jikoku_list.append(self.convert_stop_time_to_ekijikoku(stop_times_found[0]))
            else:
                eki_jikoku_list.append(None)

        return Ressya(
            houkou="Nobori" if trip["direction_id"] == 0 else "Kudari",
            syubetsu=0,
            ressyabangou=trip["trip_id"],
            eki_jikoku_list=NodeList(EkiJikoku, eki_jikoku_list),
        )

    def convert_calendar_to_dia(self, calendar_id: str) -> Dia:
        trips = self.trips[self.trips["service_id"] == calendar_id]

        ressyas = []
        for trip in trips.to_dict(orient="records"):
            ressyas.append(self.convert_trip_to_ressya(cast(Trip, trip)))

        return Dia(
            dia_name=calendar_id,
            main_back_color_index=0,
            sub_back_color_index=1,
            back_pattern_index=0,
            kudari=NodeList(
                Kudari,
                [
                    Kudari(
                        ressya_list=NodeList(
                            Ressya,
                            [r for r in ressyas if r.houkou == "Kudari"],
                        )
                    ),
                ],
            ),
            nobori=NodeList(
                Nobori,
                [
                    Nobori(
                        ressya_list=NodeList(
                            Ressya,
                            [r for r in ressyas if r.houkou == "Nobori"],
                        )
                    ),
                ],
            ),
        )

    @staticmethod
    def encode_comment(comment: str) -> str | None:
        return comment.replace("\\", "\\\\").replace("\n", "\\n")

    def convert(self) -> OuDia:
        stop_times_in_route = self.stop_times
        first_stop_times = (
            stop_times_in_route.groupby("stop_sequence").first().reset_index()[["stop_id", "stop_sequence"]]
        )

        self.sorted_stops = list(
            map(
                lambda x: cast(Stop, x),
                (
                    self.stops.merge(first_stop_times, on="stop_id", how="left", sort=False)
                    .sort_values("stop_sequence")
                    .reset_index(drop=True)
                    .to_dict(orient="records")
                ),
            )
        )

        ekis = []

        for i, stop in enumerate(self.sorted_stops):
            ekis.append(convert_stop_to_eki(cast(Stop, stop), i == 0))

        dias = []

        for calendar in self.calendars.to_dict(orient="records"):
            dias.append(self.convert_calendar_to_dia(calendar["service_id"]))

        return OuDia(
            file_type="OuDiaSecond.1.13",
            rosen=Rosen(
                rosenmei=self.route_short_name or self.route_long_name,
                kudari_dia_alias="",
                nobori_dia_alias="",
                eki_list=NodeList(
                    Eki,
                    ekis,
                ),
                ressyasyubetsu_list=NodeList(
                    Ressyasyubetsu,
                    [
                        Ressyasyubetsu(
                            syubetsumei="普通",
                            jikokuhyou_moji_color="00000000",
                            jikokuhyou_font_index=0,
                            jikokuhyou_back_color="00FFFFFF",
                            diagram_sen_color="00000000",
                            diagram_sen_style="SenStyle_Jissen",
                            stop_mark_draw_type="EStopMarkDrawType_DrawOnStop",
                        )
                    ],
                ),
                dia_list=NodeList(
                    Dia,
                    dias,
                ),
                kiten_jikoku="000",
                diagram_dgr_y_zahyou_kyori_default=60,
                operation_cross_kiten_jikoku=True,
                kijun_dia_index=0,
                comment=self.encode_comment(
                    "\n".join(
                        [
                            f"```csv:agency.txt",
                            str(
                                self.gtfs.agency.df.to_csv(
                                    index=False,
                                    na_rep="",
                                )
                            ),
                            "```",
                        ]
                        if self.gtfs.agency.df is not None
                        else []
                    )
                ),
            ),
            disp_prop=DEFAULT_DISP_PROP_OUD2,
            window_placement=DEFAULT_WINDOW_PLACEMENT_OUD2,
            file_type_app_comment="OuDia.Py",
        )


class GTFSOuDiaConverter:
    gtfs: egGTFS.egGTFS

    def __init__(self, gtfs_path: StrPath) -> None:
        self.gtfs = egGTFS.egGTFS(gtfs_path)

    def convert_gtfs_jp_to_oudia_second(self) -> list[OuDia]:
        if self.gtfs.routes.df is None:
            raise ValueError("no routes")

        result: list[OuDia] = []

        for route in self.gtfs.routes.df.replace({np.nan: None}).to_dict(orient="records"):
            rc = RouteConverter(self.gtfs, route)

            result.append(rc.convert())

        return result
