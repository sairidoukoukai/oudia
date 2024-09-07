import logging
import oudia
import pytest


def test_invalid(caplog):
    # Invalid file type
    with pytest.raises(ValueError) as e:
        oudia.loads("invalid")


def test_unsupported_software(caplog):
    caplog.set_level(logging.WARNING)
    oudia.loads("FileType=NotOuDia\nRosen.\n.\nDispProp.\n.\n")
    assert 'Unsupported software: "NotOuDia"' in caplog.text

    # # Unsupported software


EMPTY_DISP_PROP = oudia.DispProp(
    [],
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    [],
    [],
    None,
    None,
    [],
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
)


def test_pprint(capfd):
    dia = oudia.loads(
        f"FileType=OuDia.1.02\nRosen.\nRosenmei=メロンキング線\n.\nDispProp.\n.\nFileTypeAppComment=OuDia.Py 0.0.0\n"
    )
    dia.pprint()
    out, err = capfd.readouterr()
    assert (
        out
        == "  FileType=OuDia.1.02\n  Rosen.\n    Rosenmei=メロンキング線\n  .\n  DispProp.\n  .\n  FileTypeAppComment=OuDia.Py 0.0.0\n"
    )
