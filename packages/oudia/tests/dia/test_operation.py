from oudia.dia.jikoku import Jikoku
from oudia.dia.operation import (
    AfterOperationConnect,
    AfterOperationFactory,
    AfterOperationIn,
    AfterOperationJunction,
    AfterOperationNumberChange,
    AfterOperationOuter,
    AfterOperationRelease,
    AfterOperationShunt,
    BeforeOperationConnect,
    BeforeOperationFactory,
    BeforeOperationJunction,
    BeforeOperationNumberChange,
    BeforeOperationOut,
    BeforeOperationOuter,
    BeforeOperationRelease,
    BeforeOperationShunt,
    ReleasePosition,
)


import pytest


# region BeforeOperation
def test_before_operation_shunt():
    with pytest.raises(ValueError):
        BeforeOperationShunt.from_str("1/")

    operation = BeforeOperationShunt.from_str("0/0$04933/$0")
    assert operation.shunt_track_index == 0
    assert operation.hatsu_jikoku == Jikoku(2973)
    assert operation.chaku_jikoku == Jikoku(None)
    assert operation.is_display_chaku_jikoku is False

    operation = BeforeOperationShunt(
        shunt_track_index=1,
        hatsu_jikoku=Jikoku(2973),
        chaku_jikoku=Jikoku(None),
        is_display_chaku_jikoku=False,
    )
    assert str(operation) == "0/1$04933/$0"

    operation = BeforeOperationShunt(
        shunt_track_index=1,
        hatsu_jikoku=Jikoku(2973),
        chaku_jikoku=Jikoku(2983),
        is_display_chaku_jikoku=False,
    )
    assert str(operation) == "0/1$04933/04943$0"


def test_before_operation_connect():
    with pytest.raises(ValueError):
        BeforeOperationConnect.from_str("0/")

    operation = BeforeOperationConnect.from_str("1/1$04933")
    assert operation.is_connect_to_front is True
    assert operation.connect_jikoku == Jikoku(2973)

    operation = BeforeOperationConnect(is_connect_to_front=False, connect_jikoku=Jikoku(2973))
    assert str(operation) == "1/0$04933"


def test_before_operation_release():
    with pytest.raises(ValueError):
        BeforeOperationRelease.from_str("0/")

    operation = BeforeOperationRelease.from_str("2/0$1/04933")
    assert operation.release_position == 0
    assert operation.release_index_count == 1
    assert operation.release_jikoku == Jikoku(2973)

    operation = BeforeOperationRelease(
        release_position=0,
        release_index_count=1,
        release_jikoku=Jikoku(2973),
    )
    assert str(operation) == "2/0$1/04933"


def test_before_operation_out():
    with pytest.raises(ValueError):
        BeforeOperationOut.from_str("0/")

    operation = BeforeOperationOut.from_str("3/04933$InOutLink/OpNumber1;OpNumber2")
    assert operation.out_jikoku == Jikoku(2973)
    assert operation.in_out_link_code == "InOutLink"
    assert operation.operation_number_original == ["OpNumber1", "OpNumber2"]

    operation = BeforeOperationOut(
        out_jikoku=Jikoku(2973),
        in_out_link_code="InOutLink",
        operation_number_original=["OpNumber1", "OpNumber2"],
    )
    assert str(operation) == "3/04933$InOutLink/OpNumber1;OpNumber2"


def test_before_operation_outer():
    with pytest.raises(ValueError):
        BeforeOperationOuter.from_str("0/")

    with pytest.raises(ValueError):
        BeforeOperationOuter.from_str("4/")

    operation = BeforeOperationOuter.from_str("4/5$04933/04848$LinkCode/OpNumber1;OpNumber2")
    assert operation.outer_shihatsueki_index == 5
    assert operation.outer_shihatsu_jikoku == Jikoku(2973)
    assert operation.chaku_jikoku == Jikoku(2928)
    assert operation.in_out_link_code == "LinkCode"
    assert operation.operation_number_original == ["OpNumber1", "OpNumber2"]

    operation = BeforeOperationOuter(
        outer_shihatsueki_index=5,
        outer_shihatsu_jikoku=Jikoku(2973),
        chaku_jikoku=Jikoku(2928),
        in_out_link_code="LinkCode",
        operation_number_original=["OpNumber1", "OpNumber2"],
    )
    assert str(operation) == "4/5$04933/04848$LinkCode/OpNumber1;OpNumber2"


def test_before_operation_junction():
    with pytest.raises(ValueError):
        BeforeOperationJunction.from_str("0/")

    operation = BeforeOperationJunction.from_str("5/04933$OpNumber1;OpNumber2")
    assert operation.origin_jikoku == Jikoku(2973)
    assert operation.operation_number_temp == ["OpNumber1", "OpNumber2"]
    assert str(operation) == "5/04933$OpNumber1;OpNumber2"

    operation = BeforeOperationJunction(origin_jikoku=Jikoku(2973), operation_number_temp=["OpNumber1", "OpNumber2"])
    assert str(operation) == "5/04933$OpNumber1;OpNumber2"


def test_before_operation_number_change():
    with pytest.raises(ValueError):
        BeforeOperationNumberChange.from_str("0/")

    operation = BeforeOperationNumberChange.from_str("6/")
    assert operation.operation_number == []
    assert str(operation) == "6/"

    operation = BeforeOperationNumberChange.from_str("6/A;B;C")
    assert operation.operation_number == ["A", "B", "C"]
    assert str(operation) == "6/A;B;C"

    operation = BeforeOperationNumberChange.from_str("6/A;B;C;;;D;E;F")
    assert operation.operation_number == ["A", "B", "C", "D", "E", "F"]
    assert str(operation) == "6/A;B;C;D;E;F"

    operation = BeforeOperationNumberChange(operation_number=["A", "B", "C", "D", "E", "F"])
    assert str(operation) == "6/A;B;C;D;E;F"


def test_before_operation_factory():
    assert isinstance(BeforeOperationFactory.from_str("0/0$04933/$0"), BeforeOperationShunt)
    assert isinstance(BeforeOperationFactory.from_str("1/0$04933"), BeforeOperationConnect)
    assert isinstance(BeforeOperationFactory.from_str("2/0$1/04933"), BeforeOperationRelease)
    assert isinstance(BeforeOperationFactory.from_str("3/04933$InOutLink/OpNumber1"), BeforeOperationOut)
    assert isinstance(BeforeOperationFactory.from_str("4/5$04933/04848$LinkCode/OpNumber1"), BeforeOperationOuter)
    assert isinstance(BeforeOperationFactory.from_str("5/04933$OpNumber1"), BeforeOperationJunction)
    assert isinstance(BeforeOperationFactory.from_str("6/A;B;C"), BeforeOperationNumberChange)

    with pytest.raises(ValueError):
        BeforeOperationFactory.from_str("7/")
    with pytest.raises(ValueError):
        BeforeOperationFactory.from_str("-1/")
    with pytest.raises(ValueError):
        BeforeOperationFactory.from_str("ABC")


# endregion

# region AfterOperation


def test_after_operation_shunt():
    with pytest.raises(ValueError):
        AfterOperationShunt.from_str("1/")

    operation = AfterOperationShunt.from_str("0/0$04933/$0")
    assert operation.shunt_track_index == 0
    assert operation.hatsu_jikoku == Jikoku(2973)
    assert operation.chaku_jikoku == Jikoku(None)
    assert operation.is_display_hatsu_jikoku is False

    operation = AfterOperationShunt(
        shunt_track_index=0,
        hatsu_jikoku=Jikoku(2973),
        chaku_jikoku=Jikoku(None),
        is_display_hatsu_jikoku=False,
    )
    assert str(operation) == "0/0$04933/$0"


def test_after_operation_connect():
    with pytest.raises(ValueError):
        AfterOperationConnect.from_str("0/")

    operation = AfterOperationConnect.from_str("1/1$04933")
    assert operation.is_connect_to_front is True
    assert operation.connect_jikoku == Jikoku(2973)

    operation = AfterOperationConnect(is_connect_to_front=False, connect_jikoku=Jikoku(2973))
    assert str(operation) == "1/0$04933"


def test_after_operation_release():
    with pytest.raises(ValueError):
        AfterOperationRelease.from_str("0/")

    operation = AfterOperationRelease.from_str("2/0$1/04933")
    assert operation.release_position == ReleasePosition.AFTER
    assert operation.release_index_count == 1
    assert operation.release_jikoku == Jikoku(2973)

    operation = AfterOperationRelease(
        release_position=ReleasePosition.AFTER,
        release_index_count=1,
        release_jikoku=Jikoku(2973),
    )
    assert str(operation) == "2/0$1/04933"


def test_after_operation_in():
    with pytest.raises(ValueError):
        AfterOperationIn.from_str("0/")

    operation = AfterOperationIn.from_str("3/04933$")
    assert operation.in_out_link_code == ""
    assert operation.in_jikoku == Jikoku(2973)

    operation = AfterOperationIn(
        in_jikoku=Jikoku(2973),
        in_out_link_code="",
    )
    assert str(operation) == "3/04933$"


def test_after_operation_outer():
    with pytest.raises(ValueError):
        AfterOperationOuter.from_str("0/")

    with pytest.raises(ValueError):
        AfterOperationOuter.from_str("4/")

    operation = AfterOperationOuter.from_str("4/5$04933/04848$Outer1")
    assert operation.outer_terminal_index == 5
    assert operation.hatsu_jikoku == Jikoku(2973)
    assert operation.outer_terminal_jikoku == Jikoku(2928)
    assert operation.in_out_link_code == "Outer1"

    operation = AfterOperationOuter(
        outer_terminal_index=5,
        hatsu_jikoku=Jikoku(2973),
        outer_terminal_jikoku=Jikoku(2928),
        in_out_link_code="Outer1",
    )
    assert str(operation) == "4/5$04933/04848$Outer1"


def test_after_operation_junction():
    with pytest.raises(ValueError):
        AfterOperationJunction.from_str("0/")

    with pytest.raises(ValueError):
        operation = AfterOperationJunction.from_str("5/")

    with pytest.raises(ValueError):
        operation = AfterOperationJunction.from_str("5/$$")

    with pytest.raises(ValueError):
        operation = AfterOperationJunction.from_str("5/$invalid")

    with pytest.raises(ValueError):
        operation = AfterOperationJunction.from_str("5/invalid$0")

    with pytest.raises(ValueError):
        operation = AfterOperationJunction.from_str("5/04933$-1")

    with pytest.raises(ValueError):
        operation = AfterOperationJunction.from_str("5/04933$4")

    operation = AfterOperationJunction.from_str("5/04933$1")
    assert operation.terminal_jikoku == Jikoku(2973)
    assert operation.next_junction_type == 1
    assert str(operation) == "5/04933$1"

    operation = AfterOperationJunction(terminal_jikoku=Jikoku(2973), next_junction_type=1)
    assert str(operation) == "5/04933$1"


def test_after_operation_number_change():
    with pytest.raises(ValueError):
        AfterOperationNumberChange.from_str("0/")

    operation = AfterOperationNumberChange.from_str("6/")
    assert operation.operation_numbers == []
    assert operation.is_operation_number_reverse == True
    assert str(operation) == "6/"

    operation = AfterOperationNumberChange.from_str("6/A;B;C")
    assert operation.operation_numbers == ["A", "B", "C"]
    assert operation.is_operation_number_reverse == False
    assert str(operation) == "6/A;B;C"

    operation = AfterOperationNumberChange.from_str("6/A;B;C;;;D;E;F")
    assert operation.operation_numbers == ["A", "B", "C", "D", "E", "F"]
    assert operation.is_operation_number_reverse == False
    assert str(operation) == "6/A;B;C;D;E;F"

    operation = AfterOperationNumberChange(
        operation_numbers=["A", "B", "C", "D", "E", "F"],
    )
    assert operation.is_operation_number_reverse == False
    assert str(operation) == "6/A;B;C;D;E;F"


def test_after_operation_factory():
    assert isinstance(AfterOperationFactory.from_str("0/0$04933/$0"), AfterOperationShunt)
    assert isinstance(AfterOperationFactory.from_str("1/0$04933"), AfterOperationConnect)
    assert isinstance(AfterOperationFactory.from_str("2/0$1/04933"), AfterOperationRelease)
    assert isinstance(AfterOperationFactory.from_str("3/04933$0"), AfterOperationIn)
    assert isinstance(AfterOperationFactory.from_str("4/5$04933/04848$"), AfterOperationOuter)
    assert isinstance(AfterOperationFactory.from_str("5/04933$0"), AfterOperationJunction)
    assert isinstance(AfterOperationFactory.from_str("6/A;B;C"), AfterOperationNumberChange)

    with pytest.raises(ValueError):
        AfterOperationFactory.from_str("7/")
    with pytest.raises(ValueError):
        AfterOperationFactory.from_str("-1/")
    with pytest.raises(ValueError):
        AfterOperationFactory.from_str("ABC")


# endregion
