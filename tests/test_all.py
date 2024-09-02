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

def test_parser():
    assert oudia.loads("FileType=OuDia.1.02") == oudia.OuDia(file_type=oudia.FileType("OuDia", "1.02"), children=[])
    assert oudia.loads("FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.") == oudia.OuDia(
        file_type=oudia.FileType("OuDia", "1.02"),
        children=[oudia.Node("Rosen", { "Rosenmei": "メロンキング線" })]
    )

def test_exporter():
    assert oudia.dumps(oudia.OuDia(file_type=oudia.FileType("OuDia", "1.02"), children=[
        oudia.Node("Rosen", { "Rosenmei": "メロンキング線" })    
    ])) == "FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n."
