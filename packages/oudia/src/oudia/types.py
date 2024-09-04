from dataclasses import dataclass
from .nodes import Node, TypedNode


@dataclass
class FileType:
    """
    Represents a file type.

    Attributes:
        software (str): The software that created the file.
        version (str | None, optional): The version of the software. Defaults to None.
    """

    software: str
    version: str | None = None

    @staticmethod
    def from_str(text: str) -> "FileType":
        """
        Creates a `FileType` object from a given string.

        Args:
            text (str): The string to parse.

        Returns:
            FileType: The parsed `FileType` object.
        """
        return FileType(*text.split(".", 1))

    def __str__(self) -> str:
        """
        Returns a string representation of the `FileType` object.

        Returns:
            str: The string representation of the `FileType` object.
        """
        return f"{self.software}.{self.version}" if self.version else self.software


@dataclass
class OuDia:
    """
    Represents an OuDia file.

    Attributes:
        file_type (FileType): The file type of the OuDia file.
        chilren (list[Node]): The children of the OuDia file.
        aftermath (str | None, optional): The afterward text of the OuDia file. Defaults to None.
    """

    file_type: FileType
    children: list["Node | TypedNode"]
    aftermath: str | None = None

    def pprint(self, indent: int = 0, with_lines: bool = False):
        """
        Prints the OuDia file in a pretty format.

        Args:
            indent (int, optional): The indentation level. Defaults to 0.
        """
        print(
            " " * indent + str(self.file_type)
            if not with_lines
            else "|" * (indent + 1) + str(self.file_type)
        )
        for child in self.children:
            child.pprint(indent + 2)
        if self.aftermath:
            print(" " * indent + self.aftermath)
