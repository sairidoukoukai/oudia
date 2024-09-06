from oudia.dia.jikoku import Jikoku


def test_jikoku_init():
    assert Jikoku(0).total_seconds == 0
    assert Jikoku(24 * 60 * 60 - 1).total_seconds == 24 * 60 * 60 - 1
    assert Jikoku(None).total_seconds is None


def test_jikoku_wrapping():
    assert Jikoku(24 * 3600).total_seconds == 0
    assert Jikoku(24 * 3600 + 1).total_seconds == 1
    assert Jikoku(24 * 3600 * 2 - 1).total_seconds == Jikoku(24 * 3600 - 1).total_seconds
    assert Jikoku(-1).total_seconds == Jikoku(24 * 3600 - 1).total_seconds


def test_jikoku_validity():
    assert bool(Jikoku(0)) == True
    assert bool(Jikoku(24 * 3600)) == True
    assert bool(Jikoku(None)) == False


def test_jikoku_str():
    assert str(Jikoku(0)) == "00:00:00"
    assert str(Jikoku(24 * 3600 - 1)) == "23:59:59"
    assert str(Jikoku(24 * 3600)) == "00:00:00"
    assert str(Jikoku(2928)) == "00:48:48"


def test_jikoku_get_time():
    assert Jikoku(0).get_hour() == 0
    assert Jikoku(24 * 3600 - 1).get_hour() == 23

    assert Jikoku(0).get_minute() == 0
    assert Jikoku(24 * 3600 - 1).get_minute() == 59

    assert Jikoku(0).get_second() == 0
    assert Jikoku(24 * 3600 - 1).get_second() == 59


def test_jikoku_set_time():
    assert Jikoku(0).set_time(0, 0, 0).total_seconds == 0
    assert Jikoku(0).set_time(23, 59, 59).total_seconds == 24 * 3600 - 1

    assert Jikoku(24 * 3600).set_time(0, 0, 0).total_seconds == 0
    assert Jikoku(24 * 3600).set_time(23, 59, 59).total_seconds == 24 * 3600 - 1


def test_jikoku_add_seconds():
    assert Jikoku(0).add_seconds(0).total_seconds == 0
    assert Jikoku(0).add_seconds(100).total_seconds == 100

    assert Jikoku(24 * 3600).add_seconds(0).total_seconds == 0
    assert Jikoku(24 * 3600).add_seconds(2928).total_seconds == 2928

    jikoku = Jikoku(24 * 3600)
    jikoku.add_seconds(0)
    assert jikoku.total_seconds == 0
    jikoku.add_seconds(2928)
    assert jikoku.total_seconds == 2928


def test_jikoku_compare():
    assert Jikoku(0).compare(Jikoku(0)) == 0
    assert Jikoku(0).compare(Jikoku(24 * 3600)) == 0

    assert Jikoku(2928).compare(Jikoku(0)) == 1
    assert Jikoku(0).compare(Jikoku(2928)) == -1

    assert Jikoku(2928) == Jikoku(2928)
    assert Jikoku(2928) != Jikoku(2929)

    assert Jikoku(2928) < Jikoku(2929)
    assert Jikoku(2929) > Jikoku(2928)

    assert Jikoku(None) < Jikoku(0)
    assert Jikoku(0) > Jikoku(None)
    assert Jikoku(None) == Jikoku(None)


def test_jikoku_conv_init():
    assert JikokuConv().no_colon is False
    assert JikokuConv().hour == EHour.ZERO
    assert JikokuConv().second == ESecond.OUTPUT
    assert JikokuConv().second_round_chaku == ESecondRound.ROUND_DOWN
    assert JikokuConv().second_round_hatsu == ESecondRound.ROUND_DOWN
    assert JikokuConv().display_2400 is False

