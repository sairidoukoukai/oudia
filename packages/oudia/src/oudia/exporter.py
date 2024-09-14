"""OuDiaを書き込むためのモジュールです。"""

from typing import TextIO
from .nodes import OuDia


def dumps(oudia: OuDia) -> str:
    """OuDiaを文字列に書き込む"""
    return str(oudia) + "\n"


def dump(oudia: OuDia, fp: TextIO) -> None:
    """OuDiaをファイルに書き込む"""
    fp.write(dumps(oudia))
