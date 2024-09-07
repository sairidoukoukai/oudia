"""This module test the end-to-end `dump` and `dumps` functions"""

import oudia

from nodes.test_node import EMPTY_ROSEN
from test_parse import EMPTY_DISP_PROP


def test_dumps_empty():
    assert (
        oudia.dumps(
            oudia.OuDia(
                file_type=oudia.FileType("OuDia", "1.02"),
                rosen=EMPTY_ROSEN,
                disp_prop=EMPTY_DISP_PROP,
                window_placement=None,
            )
        )
        == "FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nDispProp.\n.\n"
    )


def test_exporter():
    assert (
        oudia.dumps(
            oudia.OuDia(
                file_type=oudia.FileType("OuDia", "1.02"),
                rosen=EMPTY_ROSEN,
                disp_prop=EMPTY_DISP_PROP,
                window_placement=None,
                file_type_app_comment="OuDia.Py 0.0.0",
            )
        )
        == "FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nDispProp.\n.\nFileTypeAppComment=OuDia.Py 0.0.0\n"
    )
