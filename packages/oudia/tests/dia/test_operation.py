from oudia.dia.jikoku import Jikoku
from oudia.dia.operation import BeforeOperation, BOperation, AfterOperation, AOperation


def test_before_operation_str():
    operation = BeforeOperation(
        operation=BOperation.SHUNT,
        bool_data_1=False,
        bool_data_2=False,
        int_data_1=5,
        int_data_2=0,
        int_data_3=0,
        jikoku_data_1=Jikoku(2973),
        jikoku_data_2=Jikoku(None),
        jikoku_data_3=Jikoku(None),
        operation_number_1=[],
        operation_number_2=[],
        operation_number_3=[],
        in_out_link_code="",
        before_operation_list=[],
        after_operation_list=[],
    )
    assert str(operation) == "0/5$04933/$0"

    operation = BeforeOperation(
        operation=BOperation.SHUNT,
        bool_data_1=False,
        bool_data_2=False,
        int_data_1=5,
        int_data_2=0,
        int_data_3=0,
        jikoku_data_1=Jikoku(2973),
        jikoku_data_2=Jikoku(3600),
        jikoku_data_3=Jikoku(None),
        operation_number_1=[],
        operation_number_2=[],
        operation_number_3=[],
        in_out_link_code="",
        before_operation_list=[],
        after_operation_list=[],
    )
    assert str(operation) == "0/5$04933/100$0"


def test_before_operation_shunt_from_str():
    operation = BeforeOperation.from_str("0/7$627/$0")
    assert operation.operation == BOperation.SHUNT


def test_before_operation_shunt_str_from_str():
    operation = BeforeOperation.from_str("0/7$627/$0")
    assert str(operation) == "0/7$627/$0"


def test_after_operation_shunt_str():
    operation = AfterOperation(
        operation=AOperation.SHUNT,
        bool_data_1=False,
        bool_data_2=False,
        int_data_1=5,
        int_data_2=0,
        jikoku_data_1=Jikoku(2973),
        jikoku_data_2=Jikoku(None),
        operation_number_1=[],
        operation_number_2=[],
        operation_number_3=[],
        in_out_link_code="",
        before_operation_list=[],
        after_operation_list=[],
    )

    assert str(operation) == "0/5$04933/$0"

    operation = AfterOperation(
        operation=AOperation.SHUNT,
        bool_data_1=False,
        bool_data_2=False,
        int_data_1=5,
        int_data_2=0,
        jikoku_data_1=Jikoku(2973),
        jikoku_data_2=Jikoku(3600),
        operation_number_1=[],
        operation_number_2=[],
        operation_number_3=[],
        in_out_link_code="",
        before_operation_list=[],
        after_operation_list=[],
    )

    assert str(operation) == "0/5$04933/100$0"


def test_after_operation_shunt_from_str():
    operation = AfterOperation.from_str("0/7$627/$0")
    assert operation.operation == AOperation.SHUNT


def test_after_operation_shunt_str_from_str():
    operation = AfterOperation.from_str("0/7$627/$0")
    assert str(operation) == "0/7$627/$0"


#     operation = BeforeOperation.from_str("0")
#     assert operation.ekiatsukai == Ekiatsukai.NONE


# def test_operation_str():
#     operation = BeforeOperation(
#         ekiatsukai=Ekiatsukai.TEISYA,
#         chaku_jikoku=Jikoku(3600),
#         hatsu_jikoku=Jikoku(3660),
#         ressya_track_index=None,
#         before_operation_list=[],
#         after_operation_list=[],
#     )
#     assert str(operation) == "1;100/101"

#     operation = BeforeOperation(
#         ekiatsukai=Ekiatsukai.TEISYA,
#         chaku_jikoku=Jikoku(None),
#         hatsu_jikoku=Jikoku(3600),
#         ressya_track_index=None,
#         before_operation_list=[],
#         after_operation_list=[],
#     )
#     assert str(operation) == "1;100"

#     operation = BeforeOperation(
#         ekiatsukai=Ekiatsukai.TSUUKA,
#         chaku_jikoku=Jikoku(3600),
#         hatsu_jikoku=Jikoku(None),
#         ressya_track_index=None,
#         before_operation_list=[],
#         after_operation_list=[],
#     )
#     assert str(operation) == "2;100/"

#     operation = BeforeOperation(
#         ekiatsukai=Ekiatsukai.TEISYA,
#         chaku_jikoku=Jikoku(None),
#         hatsu_jikoku=Jikoku(3660),
#         ressya_track_index=None,
#         before_operation_list=[],
#         after_operation_list=[],
#     )
#     assert str(operation) == "1;101"

#     operation = BeforeOperation(
#         ekiatsukai=Ekiatsukai.TEISYA,
#         chaku_jikoku=Jikoku(3600),
#         hatsu_jikoku=Jikoku(3660),
#         ressya_track_index=3,
#         before_operation_list=[],
#         after_operation_list=[],
#     )

#     assert str(operation) == "1;100/101$3"
#     operation = BeforeOperation(
#         ekiatsukai=Ekiatsukai.TEISYA,
#         chaku_jikoku=Jikoku(2928),
#         hatsu_jikoku=Jikoku(3669),
#         ressya_track_index=3,
#         before_operation_list=[],
#         after_operation_list=[],
#     )
#     assert str(operation) == "1;04848/10109$3"

#     operation = BeforeOperation(
#         ekiatsukai=Ekiatsukai.TEISYA,
#         chaku_jikoku=Jikoku(None),
#         hatsu_jikoku=Jikoku(None),
#         ressya_track_index=5,
#         before_operation_list=[],
#         after_operation_list=[],
#     )
#     assert str(operation) == "1$5"


# def test_operation_from_str():
#     eki_track_count = 5

#     operation = BeforeOperation.from_str("1;100/101$3")
#     assert operation.ekiatsukai == Ekiatsukai.TEISYA
#     assert operation.chaku_jikoku.total_seconds == 3600
#     assert operation.hatsu_jikoku.total_seconds == 3660
#     assert operation.ressya_track_index == 3

#     operation = BeforeOperation.from_str("1;100/")
#     assert operation.ekiatsukai == Ekiatsukai.TEISYA
#     assert operation.chaku_jikoku.total_seconds == 3600
#     assert bool(operation.hatsu_jikoku) is False
#     assert operation.ressya_track_index == None

#     operation = BeforeOperation.from_str("1;101")
#     assert operation.ekiatsukai == Ekiatsukai.TEISYA
#     assert bool(operation.chaku_jikoku) == False
#     assert operation.hatsu_jikoku.total_seconds == 3660
#     assert operation.ressya_track_index == None

#     operation = BeforeOperation.from_str("1$3")
#     assert operation.ekiatsukai == Ekiatsukai.TEISYA
#     assert bool(operation.chaku_jikoku) == False
#     assert bool(operation.hatsu_jikoku) == False
#     assert operation.ressya_track_index == 3

#     operation = BeforeOperation.from_str("1$6")
#     assert operation.ressya_track_index == 6

#     operation = BeforeOperation.from_str("0")
#     assert operation.ekiatsukai == Ekiatsukai.NONE
#     assert bool(operation.chaku_jikoku) == False
#     assert bool(operation.hatsu_jikoku) == False
#     assert operation.ressya_track_index == None

#     with pytest.raises(IndexError):
#         BeforeOperation.from_str("")

#     with pytest.raises(ValueError):
#         operation = BeforeOperation.from_str("1;invalid/invalid$3")


def test_operation_str_number_change():
    operation = BeforeOperation(
        operation=BOperation.NUMBER_CHANGE,
        bool_data_1=False,
        bool_data_2=False,
        int_data_1=5,
        int_data_2=0,
        int_data_3=0,
        jikoku_data_1=Jikoku(2973),
        jikoku_data_2=Jikoku(None),
        jikoku_data_3=Jikoku(None),
        operation_number_1=[],
        operation_number_2=[],
        operation_number_3=[],
        in_out_link_code="",
        before_operation_list=[],
        after_operation_list=[],
    )

    assert str(operation) == "6/"


def test_before_operation_number_change_from_str():
    operation = BeforeOperation.from_str("6/")
    assert operation.operation == BOperation.NUMBER_CHANGE

    operation = BeforeOperation.from_str("6/0$")
    assert operation.operation == BOperation.NUMBER_CHANGE
    assert operation.int_data_1 == 0


def test_after_operation_number_change_from_str():
    operation = AfterOperation.from_str("6/")
    assert operation.operation == AOperation.NUMBER_CHANGE

    operation = AfterOperation.from_str("6/0$")
    assert operation.operation == AOperation.NUMBER_CHANGE
    assert operation.int_data_1 == 0


def test_after_operation_number_change_to_str():
    operation = AfterOperation(
        operation=AOperation.NUMBER_CHANGE,
        bool_data_1=False,
        bool_data_2=False,
        int_data_1=5,
        int_data_2=0,
        jikoku_data_1=Jikoku(2973),
        jikoku_data_2=Jikoku(None),
        operation_number_1=[],
        operation_number_2=[],
        operation_number_3=[],
        in_out_link_code="",
        before_operation_list=[],
        after_operation_list=[],
    )

    assert str(operation) == "6/"
