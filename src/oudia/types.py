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

# @dataclass
# class Rosen:
#     """
#     Represents the "Rosen" (Route) section of an OuDia file.
    
#     Attributes:
#         rosenmei (str): The "Rosenmei" (Route Name) of the route.
#     """
    
#     rosenmei: str


class Node:
    """
    Represents a node in an OuDia file.

    Attributes:
        type (str): The type of the node.
        attributes (dict[str, str]): The attributes of the node.
        children (list[Node]): The children of the node.
    """
    
    type: str
    attributes: dict[str, str]
    children: list['Node']

    def __init__(self, type: str, attributes: dict[str, str] | None = None, children: list['Node'] | None = None):
        """
        Initializes a new instance of the Node class.

        Args:
            type (str): The type of the node.
            attributes (dict[str, str] | None, optional): The attributes of the node. Defaults to None.
        """
        self.type = type
        self.attributes = attributes or {}
        self.children = children or []
    
    def add_child(self, node: 'Node'):
        """
        Adds a child to the node.

        Args:
            node (Node): The node to add.
        """
        self.children.append(node)

    def __str__(self):
        """
        Returns a serialized string representation of the node.        

        Returns:
            str: The string representation of the node.
        """
        attributes = "\n".join([f"{key}={value}" for key, value in self.attributes.items()])
        children = "\n".join([str(child) for child in self.children])
        
        return f"{self.type}.\n{attributes}\n{children}."
    
    def __repr__(self) -> str:
        """
        Returns a canonical string representation of the node.

        Returns:
            str: The string representation of the node.
        """
        return f"Node(type={repr(self.type)}, attributes={repr(self.attributes)}, children={repr(self.children)})"
    
    def __eq__(self, value: object) -> bool:
        """
        Returns a boolean indicating whether the node is equal to the given value.
        
        Args:
            value (object): The value to compare with.

        Returns:
            bool: True if the node is equal to the given value, False otherwise.
        """
        return repr(self) == repr(value)
    def pprint(self, indent: int = 0):
        """
        Prints the node in a pretty format.

        Args:
            indent (int, optional): The indentation level. Defaults to 0.
        """
        print(" " * indent + self.type)
        for key, value in self.attributes.items():
            print(" " * (indent + 2) + f"{key}={value}")
        for child in self.children:
            child.pprint(indent + 2)

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
    children: list[Node]
    aftermath: str | None = None
    
    def pprint(self, indent: int = 0, with_lines: bool = False):
        """
        Prints the OuDia file in a pretty format.

        Args:
            indent (int, optional): The indentation level. Defaults to 0.
        """
        print(" " * indent + str(self.file_type) if not with_lines else "|" * (indent + 1) + str(self.file_type))
        for child in self.children:
            child.pprint(indent + 2)
        if self.aftermath:
            print(" " * indent + self.aftermath)
