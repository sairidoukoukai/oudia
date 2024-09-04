from typing import TextIO
from .nodes import OuDia


def dumps(oudia: OuDia) -> str:
    # Add a newline at the end of the file
    return str(oudia) + "\n"


def dump(oudia: OuDia, fp: TextIO) -> None:
    fp.write(dumps(oudia))
