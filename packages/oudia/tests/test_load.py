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
    assert 'Unsupported software: "NotOuDia"' in caplog.text

    # # Unsupported software
