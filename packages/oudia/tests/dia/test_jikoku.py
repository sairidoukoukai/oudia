import pytest

from oudia.dia.jikoku import Hour, Second, SecondRound, Jikoku, JikokuConv


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
    assert JikokuConv().hour == Hour.ZERO
    assert JikokuConv().second == Second.OUTPUT
    assert JikokuConv().second_round_chaku == SecondRound.ROUND_DOWN
    assert JikokuConv().second_round_hatsu == SecondRound.ROUND_DOWN
    assert JikokuConv().display_2400 is False


def test_jikoku_conv_encode_default():
    default_jikoku_conv = JikokuConv()

    assert default_jikoku_conv.encode(Jikoku(0)) == "00:00:00"
    assert default_jikoku_conv.encode(Jikoku(24 * 3600)) == "00:00:00"
    assert default_jikoku_conv.encode(Jikoku(24 * 3600 - 1)) == "23:59:59"

    assert default_jikoku_conv.encode(Jikoku(2928)) == "00:48:48"
    assert default_jikoku_conv.encode(Jikoku(3600)) == "01:00:00"
    assert default_jikoku_conv.encode(Jikoku(3601)) == "01:00:01"

    assert default_jikoku_conv.encode(Jikoku(0), False) == "00:00:00"
    assert default_jikoku_conv.encode(Jikoku(0), True) == "00:00:00"

    assert default_jikoku_conv.encode(Jikoku(1), False) == "00:00:01"
    assert default_jikoku_conv.encode(Jikoku(1), True) == "00:00:01"

    assert default_jikoku_conv.encode(Jikoku(24 * 3600 - 1), False, Jikoku(0)) == "23:59:59"
    assert default_jikoku_conv.encode(Jikoku(24 * 3600 - 1), False, Jikoku(24 * 3600)) == "23:59:59"

    assert default_jikoku_conv.encode(Jikoku(24 * 3600 - 1), True, Jikoku(0)) == "23:59:59"
    assert default_jikoku_conv.encode(Jikoku(24 * 3600 - 1), True, Jikoku(24 * 3600)) == "23:59:59"


def test_jikoku_conv_encode_no_colon():
    conv_no_colon = JikokuConv(no_colon=True)

    assert conv_no_colon.encode(Jikoku(3661), True, Jikoku(0)) == "010101"  # No colon between hour, minute, and second


def test_jikoku_conv_encode_no_second():
    conv_no_second = JikokuConv(second=Second.NO_SECOND)
    assert conv_no_second.encode(Jikoku(3661), True, Jikoku(0)) == "01:01"  # No second

    conv_not_if_zero = JikokuConv(second=Second.NOT_IF_ZERO)
    assert conv_not_if_zero.encode(Jikoku(3661), True, Jikoku(0)) == "01:01:01"
    assert conv_not_if_zero.encode(Jikoku(0), True, Jikoku(0)) == "00:00"


def test_jikoku_conv_encode_no_colon_no_second():
    conv_no_colon_no_second = JikokuConv(no_colon=True, second=Second.NO_SECOND)
    assert conv_no_colon_no_second.encode(Jikoku(3661), True, Jikoku(0)) == "0101"  # No colon and no seconds


def test_jikoku_conv_encode_rounding():
    conv_round_up = JikokuConv(second=Second.NO_SECOND, second_round_chaku=SecondRound.ROUND_UP)
    assert conv_round_up.encode(Jikoku(3661), True, Jikoku(0)) == "01:02"  # Rounded up to next minute

    conv_round_down = JikokuConv(second=Second.NO_SECOND, second_round_hatsu=SecondRound.ROUND_DOWN)
    assert conv_round_down.encode(Jikoku(3661), True, Jikoku(0)) == "01:01"  # Rounded down to next minute

    conv_round = JikokuConv(
        second=Second.NO_SECOND, second_round_chaku=SecondRound.ROUND, second_round_hatsu=SecondRound.ROUND
    )
    assert conv_round.encode(Jikoku(3661), True, Jikoku(0)) == "01:01"
    assert conv_round.encode(Jikoku(3661), False, Jikoku(0)) == "01:01"


def test_jikoku_conv_encode_hour():
    conv = JikokuConv(hour=Hour.ZERO)
    assert conv.encode(Jikoku(3600), True, Jikoku(0)) == "01:00:00"
    assert conv.encode(Jikoku(3661), True, Jikoku(0)) == "01:01:01"

    conv = JikokuConv(hour=Hour.ZERO_TO_NONE)
    assert conv.encode(Jikoku(3600), True, Jikoku(0)) == "1:00:00"
    assert conv.encode(Jikoku(3661), True, Jikoku(0)) == "1:01:01"

    conv = JikokuConv(hour=Hour.ZERO_TO_SPACE)
    assert conv.encode(Jikoku(3600), True, Jikoku(0)) == " 1:00:00"
    assert conv.encode(Jikoku(3661), True, Jikoku(0)) == " 1:01:01"


def test_jikoku_conv_encode_display_2400():
    conv = JikokuConv(display_2400=True)
    assert conv.encode(Jikoku(3600), True, Jikoku(0)) == "01:00:00"
    assert conv.encode(Jikoku(3661), True, Jikoku(0)) == "01:01:01"

    assert conv.encode(Jikoku(24 * 3600), True, Jikoku(0)) == "24:00:00"
    assert conv.encode(Jikoku(24 * 3600 + 1), True, Jikoku(0)) == "24:00:01"


def test_jikoku_conv_encode_rounding_add_59():
    conv_round_up_chaku = JikokuConv(second=Second.NO_SECOND, second_round_chaku=SecondRound.ROUND_UP)
    assert conv_round_up_chaku.encode(Jikoku(3661), True, Jikoku(0)) == "01:02"
    assert conv_round_up_chaku.encode(Jikoku(3661), True) == "01:02"

    conv_round_up_hatsu = JikokuConv(second=Second.NO_SECOND, second_round_hatsu=SecondRound.ROUND_UP)
    assert conv_round_up_hatsu.encode(Jikoku(3661), False, Jikoku(0)) == "01:02"
    assert conv_round_up_hatsu.encode(Jikoku(3661), False) == "01:02"


def test_jikoku_conv_encode_rounding_add_30():
    conv_round_chaku = JikokuConv(second=Second.NO_SECOND, second_round_chaku=SecondRound.ROUND)
    assert conv_round_chaku.encode(Jikoku(3630), True, Jikoku(0)) == "01:01"
    assert conv_round_chaku.encode(Jikoku(3630), True, None) == "01:01"

    conv_round_hatsu = JikokuConv(second=Second.NO_SECOND, second_round_hatsu=SecondRound.ROUND)
    assert conv_round_hatsu.encode(Jikoku(3630), False, Jikoku(0)) == "01:01"
    assert conv_round_hatsu.encode(Jikoku(3630), False, None) == "01:01"


def test_jikoku_conv_encode_skip_rounding():
    conv_skip_rounding = JikokuConv(second_round_chaku=SecondRound.ROUND_UP)
    assert conv_skip_rounding.encode(Jikoku(18030), True, Jikoku(18020)) == "05:00:30"

    conv_round_down_hatsu = JikokuConv(second_round_hatsu=SecondRound.ROUND_DOWN)
    assert conv_round_down_hatsu.encode(Jikoku(18030), False, Jikoku(18030)) == "05:00:30"

    assert conv_skip_rounding.encode(Jikoku(18020), True, Jikoku(18020)) == "05:00:20"

    conv_no_second_roundup_up = JikokuConv(second=Second.NO_SECOND, second_round_chaku=SecondRound.ROUND_UP)
    assert conv_no_second_roundup_up.encode(Jikoku(18020), True, Jikoku(18020)) == "05:00"

    assert conv_no_second_roundup_up.encode(Jikoku(18020), False, Jikoku(18035)) == "05:00"

    assert conv_no_second_roundup_up.encode(Jikoku(18020), True, Jikoku(18035)) == "05:00"

    #                     elif (
    #     is_chaku_jikoku
    #     and self.second_round_chaku == SecondRound.ROUND_UP
    #     and jikoku.get_second() < 30
    #     and compare_jikoku.get_second() >= 30
    # ):
    #     if jikoku.get_second() + compare_jikoku.get_second() >= 60:
    #         temp_jikoku.add_seconds(59)
    assert conv_no_second_roundup_up.encode(Jikoku(18020), False, Jikoku(18035)) == "05:00"

    #     if (
    #     is_chaku_jikoku
    #     and self.second_round_chaku == SecondRound.ROUND_UP
    #     and jikoku.get_second() > 0
    #     and jikoku.get_second() < 30
    #     and compare_jikoku.get_second() > 0
    #     and compare_jikoku.get_second() < 30
    # ):
    #     pass  # Skip rounding
    # elif (
    #     not is_chaku_jikoku
    #     and self.second_round_hatsu == SecondRound.ROUND_DOWN
    #     and jikoku.get_second() >= 30
    #     and compare_jikoku.get_second() >= 30
    # ):
    #     temp_jikoku.add_seconds(59)
    # elif (
    #     is_chaku_jikoku
    #     and self.second_round_chaku == SecondRound.ROUND_UP
    #     and jikoku.get_second() < 30
    #     and compare_jikoku.get_second() >= 30
    # ):
    #     if jikoku.get_second() + compare_jikoku.get_second() >= 60:
    #         temp_jikoku.add_seconds(59)

    assert conv_no_second_roundup_up.encode(Jikoku(18020), False, Jikoku(18035)) == "05:00"
    assert conv_no_second_roundup_up.encode(Jikoku(18020), True, Jikoku(18035)) == "05:00"
    assert conv_no_second_roundup_up.encode(Jikoku(18020), False, Jikoku(18035)) == "05:00"

    conv_no_second_rounddown_down = JikokuConv(second=Second.NO_SECOND, second_round_hatsu=SecondRound.ROUND_DOWN)
    assert conv_no_second_rounddown_down.encode(Jikoku(18020), False, Jikoku(18035)) == "05:00"
    assert conv_no_second_rounddown_down.encode(Jikoku(18020), True, Jikoku(18035)) == "05:00"
    assert conv_no_second_rounddown_down.encode(Jikoku(18020), False, Jikoku(18035)) == "05:00"
    assert conv_no_second_rounddown_down.encode(Jikoku(18020), True, Jikoku(18035)) == "05:00"
    assert conv_no_second_rounddown_down.encode(Jikoku(18020), False, Jikoku(18035)) == "05:00"


def test_jikoku_conv_encode_sum_rounding():
    conv = JikokuConv(second=Second.NO_SECOND, second_round_chaku=SecondRound.ROUND_UP)

    assert conv.encode(Jikoku(17930), True, Jikoku(18031)) == "04:59"

    conv = JikokuConv(second=Second.NO_SECOND, second_round_chaku=SecondRound.ROUND_DOWN)

    assert conv.encode(Jikoku(17930), True, Jikoku(18031)) == "04:58"

    conv = JikokuConv(second=Second.NO_SECOND, second_round_hatsu=SecondRound.ROUND_DOWN)

    assert conv.encode(Jikoku(17930), True, Jikoku(18031)) == "04:58"

    conv = JikokuConv(second=Second.NO_SECOND, second_round_hatsu=SecondRound.ROUND_UP)

    assert conv.encode(Jikoku(17930), True, Jikoku(18031)) == "04:58"

    conv = JikokuConv(second=Second.NO_SECOND, second_round_hatsu=SecondRound.ROUND_DOWN)
    assert conv.encode(Jikoku(17930), True, Jikoku(18031)) == "04:58"
    assert conv.encode(Jikoku(17930), False, Jikoku(18031)) == "04:58"


def test_jikoku_conv_encode_sum_rounding2():
    conv = JikokuConv(
        second=Second.NO_SECOND, second_round_hatsu=SecondRound.ROUND_DOWN, second_round_chaku=SecondRound.ROUND_DOWN
    )
    assert conv.encode(Jikoku(3635), False, Jikoku(3636)) == "01:01"

    # is_chaku_jikoku
    # and self.second_round_chaku == SecondRound.ROUND_UP
    #     and self.second_round_hatsu == SecondRound.ROUND_DOWN
    #     and jikoku.get_second() >= 30
    #     and compare_jikoku.get_second() >= 30
    #     and not self.second_round_chaku == SecondRound.ROUND_UP
    #     and not jikoku.get_second() > 0
    #     and not jikoku.get_second() < 30
    #     and not compare_jikoku.get_second() > 0
    #     and not compare_jikoku.get_second() < 30
    #     and jikoku.get_hour() == compare_jikoku.get_hour()
    #     and jikoku.get_minute() == compare_jikoku.get_minute()
    #     and compare_jikoku

    conv = JikokuConv(
        second=Second.NO_SECOND, second_round_hatsu=SecondRound.ROUND_DOWN, second_round_chaku=SecondRound.ROUND_UP
    )
    assert conv.encode(Jikoku(3615), True, Jikoku(3648)) == "01:01"

    #     and self.second == Second.NO_SECOND


def test_jikoku_conv_encode_sum_rounding_add_59():
    conv_add_59 = JikokuConv(second_round_chaku=SecondRound.ROUND_UP)
    assert conv_add_59.encode(Jikoku(17930), True, Jikoku(18031)) == "04:58:50"


def test_jikoku_conv_decode_default():
    default_jikoku_conv = JikokuConv()

    assert default_jikoku_conv.decode("00:00:00").total_seconds == 0
    assert default_jikoku_conv.decode("23:59:59").total_seconds == 24 * 3600 - 1
    assert default_jikoku_conv.decode("01:00:00").total_seconds == 3600
    assert default_jikoku_conv.decode("01:01:01").total_seconds == 3661
    assert default_jikoku_conv.decode("00:48:48").total_seconds == 2928


def test_jikoku_conv_decode_no_second():
    conv_no_second = JikokuConv(second=Second.NO_SECOND)
    assert conv_no_second.decode("01:01").total_seconds == 3660
    assert conv_no_second.decode("01:01:00").total_seconds == 3660
    assert conv_no_second.decode("01:01:01").total_seconds == 3661

    conv_no_second_if_zero = JikokuConv(second=Second.NOT_IF_ZERO)
    assert conv_no_second_if_zero.decode("01:01").total_seconds == 3660
    assert conv_no_second_if_zero.decode("01:01:00").total_seconds == 3660
    assert conv_no_second_if_zero.decode("01:01:01").total_seconds == 3661


def test_jikoku_conv_decode_display_2400():
    conv_display_2400_off = JikokuConv(display_2400=False)
    conv_display_2400_on = JikokuConv(display_2400=True)
    assert conv_display_2400_off.decode("24:00:00", is_chaku_jikoku=True).total_seconds == 0
    assert conv_display_2400_off.decode("24:00:00", is_chaku_jikoku=False).total_seconds == 0
    assert conv_display_2400_on.decode("24:00:00", is_chaku_jikoku=True).total_seconds == 0
    assert conv_display_2400_on.decode("24:00:00", is_chaku_jikoku=False).total_seconds == 0


def test_jikoku_conv_decode_hour():
    conv_has_leading_zero = JikokuConv(hour=Hour.ZERO)
    assert conv_has_leading_zero.decode("01:00:00").total_seconds == 3600

    conv_no_leading_zero = JikokuConv(hour=Hour.ZERO_TO_NONE)
    assert conv_no_leading_zero.decode("1:00:00").total_seconds == 3600

    conv_zero_to_space = JikokuConv(hour=Hour.ZERO_TO_SPACE)
    assert conv_zero_to_space.decode(" 1:01:01").total_seconds == 3661


def test_jikoku_conv_decode_no_colon():
    conv_no_colon = JikokuConv(no_colon=True)

    assert conv_no_colon.decode("010101").total_seconds == 3661
    assert conv_no_colon.decode("0101").total_seconds == 3660


def test_jikoku_conv_decode_overflowed():
    conv = JikokuConv()
    assert conv.decode("25:00:00") == Jikoku(24 * 3600 + 3600)


def test_jikoku_conv_decode_rounding():
    conv_round_up = JikokuConv(second=Second.NO_SECOND, second_round_chaku=SecondRound.ROUND_UP)
    assert conv_round_up.decode("01:02").total_seconds == 3720

    conv_round_down = JikokuConv(second=Second.NO_SECOND, second_round_hatsu=SecondRound.ROUND_DOWN)
    assert conv_round_down.decode("01:01").total_seconds == 3660  # Rounding down to previous minute


def test_jikoku_conv_decode_no_colon_no_second():
    conv_no_colon_no_second = JikokuConv(no_colon=True, second=Second.NO_SECOND)

    assert conv_no_colon_no_second.decode("0101").total_seconds == 3660
    assert conv_no_colon_no_second.decode("0100").total_seconds == 3600


def test_jikoku_conv_decode_no_colon_no_second_no_leading_zero():
    conv_no_colon_no_second = JikokuConv(no_colon=True, second=Second.NO_SECOND, hour=Hour.ZERO_TO_NONE)

    assert conv_no_colon_no_second.decode("101").total_seconds == 3660
    assert conv_no_colon_no_second.decode("100").total_seconds == 3600


def test_jikoku_conv_decode_invalid():
    conv = JikokuConv()

    assert conv.decode("") == Jikoku(None)

    # Test invalid time string formats
    with pytest.raises(ValueError):
        conv.decode("invalid")

    with pytest.raises(ValueError):
        conv.decode("24:61:00")

    with pytest.raises(ValueError):
        conv.decode("24:00:60")  # Invalid second (greater than 59)

    with pytest.raises(ValueError):
        conv.decode("012")  # Invalid length without colon

    with pytest.raises(ValueError):
        conv.decode("12345")  # Too few or too many digits without colon

    with pytest.raises(ValueError):
        conv.decode("12:75")  # Invalid minute

    with pytest.raises(ValueError):
        conv.decode("aa:bb")  # Invalid non-numeric input

    conv_no_colon = JikokuConv(no_colon=True)
    with pytest.raises(ValueError):
        conv_no_colon.decode("67890")

    with pytest.raises(ValueError):
        conv_no_colon.decode("12:345")

    assert conv_no_colon.decode("0101") == Jikoku(3660)
    assert conv_no_colon.decode("120101") == Jikoku(43261)


def test_jikoku_conv_decode_reverse_rounding():
    conv_round_up_chaku = JikokuConv(second=Second.NO_SECOND, second_round_chaku=SecondRound.ROUND_UP)
    assert conv_round_up_chaku.decode("01:02", True) == Jikoku(3661)

    conv_round_up_hatsu = JikokuConv(second=Second.NO_SECOND, second_round_hatsu=SecondRound.ROUND_UP)
    assert conv_round_up_hatsu.decode("01:02", False) == Jikoku(3661)

    conv_round_chaku = JikokuConv(second=Second.NO_SECOND, second_round_chaku=SecondRound.ROUND)
    assert conv_round_chaku.decode("01:01", True) == Jikoku(3630)

    conv_round_hatsu = JikokuConv(second=Second.NO_SECOND, second_round_hatsu=SecondRound.ROUND)
    assert conv_round_hatsu.decode("01:01", False) == Jikoku(3630)
