from typing import TextIO
from oudia.types import OuDia


def dumps(oudia: OuDia) -> str:
    result = ""
    
    result += "FileType=" + str(oudia.file_type)
    
    if oudia.children:
        result += "\n"
    
    for node in oudia.children:
        result += str(node)
    
    if oudia.aftermath:
        result += "\n"
        result += oudia.aftermath
    
    return result

def dump(oudia: OuDia, fp: TextIO) -> None:
    fp.write(dumps(oudia))