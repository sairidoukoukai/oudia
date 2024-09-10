"""This module test the end-to-end `load` and `loads` functions"""

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
    assert 'Unsupported file format: "NotOuDia", some features may not work correctly.' in caplog.text

    # # Unsupported software


def test_utf8_bom_by_utf8():
    assert oudia.loads(
        "FileType=NotOuDia\nRosen.\n.\nDispProp.\n.\n".encode("utf-8-sig").decode("utf-8")
    ) == oudia.loads("FileType=NotOuDia\nRosen.\n.\nDispProp.\n.\n")
