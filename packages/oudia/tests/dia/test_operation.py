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


def test_before_operation_shunt_from_str():
    operation = BeforeOperation.from_str("0/7$627/$0")
    assert operation.operation == BOperation.SHUNT
    print(repr(operation))


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


def test_after_operation_shunt_from_str():
    operation = AfterOperation.from_str("0/7$627/$0")
    assert operation.operation == AOperation.SHUNT


def test_after_operation_shunt_str_from_str():
    operation = AfterOperation.from_str("0/7$627/$0")
    assert str(operation) == "0/7$627/$0"
