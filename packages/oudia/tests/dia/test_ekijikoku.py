from oudia.dia.eki_jikoku import EkiJikoku, Ekiatsukai
from oudia.dia.jikoku import Jikoku
import pytest


def test_ekijikoku_ekiatsukai_none_str():
    eki_jikoku = EkiJikoku(
        ekiatsukai=Ekiatsukai.NONE,
        chaku_jikoku=Jikoku(None),
        hatsu_jikoku=Jikoku(None),
        ressya_track_index=None,
        before_operation_list=[],
        after_operation_list=[],
    )
    assert str(eki_jikoku) == "0"


def test_ekijikoku_ekiatsukai_none_from_str():
    eki_jikoku = EkiJikoku.from_str("0")
    assert eki_jikoku.ekiatsukai == Ekiatsukai.NONE


def test_ekijikoku_str():
    eki_jikoku = EkiJikoku(
        ekiatsukai=Ekiatsukai.TEISYA,
        chaku_jikoku=Jikoku(3600),
        hatsu_jikoku=Jikoku(3660),
        ressya_track_index=None,
        before_operation_list=[],
        after_operation_list=[],
    )
    assert str(eki_jikoku) == "1;100/101"

    eki_jikoku = EkiJikoku(
        ekiatsukai=Ekiatsukai.TEISYA,
        chaku_jikoku=Jikoku(None),
        hatsu_jikoku=Jikoku(3600),
        ressya_track_index=None,
        before_operation_list=[],
        after_operation_list=[],
    )
    assert str(eki_jikoku) == "1;100"

    eki_jikoku = EkiJikoku(
        ekiatsukai=Ekiatsukai.TSUUKA,
        chaku_jikoku=Jikoku(3600),
        hatsu_jikoku=Jikoku(None),
        ressya_track_index=None,
        before_operation_list=[],
        after_operation_list=[],
    )
    assert str(eki_jikoku) == "2;100/"

    eki_jikoku = EkiJikoku(
        ekiatsukai=Ekiatsukai.TEISYA,
        chaku_jikoku=Jikoku(None),
        hatsu_jikoku=Jikoku(3660),
        ressya_track_index=None,
        before_operation_list=[],
        after_operation_list=[],
    )
    assert str(eki_jikoku) == "1;101"

    eki_jikoku = EkiJikoku(
        ekiatsukai=Ekiatsukai.TEISYA,
        chaku_jikoku=Jikoku(3600),
        hatsu_jikoku=Jikoku(3660),
        ressya_track_index=3,
        before_operation_list=[],
        after_operation_list=[],
    )

    assert str(eki_jikoku) == "1;100/101$3"
    eki_jikoku = EkiJikoku(
        ekiatsukai=Ekiatsukai.TEISYA,
        chaku_jikoku=Jikoku(2928),
        hatsu_jikoku=Jikoku(3669),
        ressya_track_index=3,
        before_operation_list=[],
        after_operation_list=[],
    )
    assert str(eki_jikoku) == "1;04848/10109$3"

    eki_jikoku = EkiJikoku(
        ekiatsukai=Ekiatsukai.TEISYA,
        chaku_jikoku=Jikoku(None),
        hatsu_jikoku=Jikoku(None),
        ressya_track_index=5,
        before_operation_list=[],
        after_operation_list=[],
    )
    assert str(eki_jikoku) == "1$5"


def test_ekijikoku_from_str():
    eki_track_count = 5

    eki_jikoku = EkiJikoku.from_str("1;100/101$3")
    assert eki_jikoku.ekiatsukai == Ekiatsukai.TEISYA
    assert eki_jikoku.chaku_jikoku.total_seconds == 3600
    assert eki_jikoku.hatsu_jikoku.total_seconds == 3660
    assert eki_jikoku.ressya_track_index == 3

    eki_jikoku = EkiJikoku.from_str("1;100/")
    assert eki_jikoku.ekiatsukai == Ekiatsukai.TEISYA
    assert eki_jikoku.chaku_jikoku.total_seconds == 3600
    assert bool(eki_jikoku.hatsu_jikoku) is False
    assert eki_jikoku.ressya_track_index == None

    eki_jikoku = EkiJikoku.from_str("1;101")
    assert eki_jikoku.ekiatsukai == Ekiatsukai.TEISYA
    assert bool(eki_jikoku.chaku_jikoku) == False
    assert eki_jikoku.hatsu_jikoku.total_seconds == 3660
    assert eki_jikoku.ressya_track_index == None

    eki_jikoku = EkiJikoku.from_str("1$3")
    assert eki_jikoku.ekiatsukai == Ekiatsukai.TEISYA
    assert bool(eki_jikoku.chaku_jikoku) == False
    assert bool(eki_jikoku.hatsu_jikoku) == False
    assert eki_jikoku.ressya_track_index == 3

    eki_jikoku = EkiJikoku.from_str("1$6")
    assert eki_jikoku.ressya_track_index == 6

    eki_jikoku = EkiJikoku.from_str("0")
    assert eki_jikoku.ekiatsukai == Ekiatsukai.NONE
    assert bool(eki_jikoku.chaku_jikoku) == False
    assert bool(eki_jikoku.hatsu_jikoku) == False
    assert eki_jikoku.ressya_track_index == None

    with pytest.raises(IndexError):
        EkiJikoku.from_str("")

    with pytest.raises(ValueError):
        eki_jikoku = EkiJikoku.from_str("1;invalid/invalid$3")
