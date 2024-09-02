from dataclasses import dataclass

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
    """

    file_type: FileType
