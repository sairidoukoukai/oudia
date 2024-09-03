import logging
import oudia
import pytest

def test_invalid(caplog):
    # Invalid file type
    with pytest.raises(ValueError) as e:
        oudia.loads("invalid")
    
    # Unsupported software
    oudia.loads("FileType=NotOuDia")
    caplog.set_level(logging.WARNING)
    assert "Unsupported software: \"NotOuDia\"" in caplog.text

def test_node_conversion():
    untyped_rosen_node = oudia.Node("Rosen", { "Rosenmei": "メロンキング線" })
    typed_rosen_node = oudia.Rosen("メロンキング線", [])
    
    assert untyped_rosen_node == typed_rosen_node.to_node()
    assert typed_rosen_node.from_node(untyped_rosen_node) == typed_rosen_node
    assert untyped_rosen_node == typed_rosen_node

def test_parser():
    assert oudia.loads("FileType=OuDia.1.02") == oudia.OuDia(file_type=oudia.FileType("OuDia", "1.02"), children=[])
    assert oudia.loads("FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.") == oudia.OuDia(
        file_type=oudia.FileType("OuDia", "1.02"),
        children=[oudia.Node("Rosen", { "Rosenmei": "メロンキング線" })]
    )
    assert oudia.loads("FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nAfterMath=Hello") == oudia.OuDia(
        file_type=oudia.FileType("OuDia", "1.02"),
        children=[oudia.Node("Rosen", { "Rosenmei": "メロンキング線" })],
        aftermath="AfterMath=Hello"
    )
    
    with open("./tests/test2.oud", "r") as f:
        dia = oudia.load(f)
        print(dia)
        print(dia.pprint())

def test_exporter():
    assert oudia.dumps(oudia.OuDia(file_type=oudia.FileType("OuDia", "1.02"), children=[
        oudia.Node("Rosen", { "Rosenmei": "メロンキング線" })    
    ])) == "FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n."

    assert oudia.dumps(oudia.OuDia(
        file_type=oudia.FileType("OuDia", "1.02"),
        children=[
            oudia.Node("Rosen", { "Rosenmei": "メロンキング線" })    
        ],
        aftermath="AfterMath=Hello"
    )) == "FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nAfterMath=Hello"
