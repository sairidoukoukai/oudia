from abc import ABC
from dataclasses import dataclass
from enum import Enum
from io import TextIOBase
from typing import Generic, Iterable, Iterator, TypeAlias, TypeVar
from csv import DictWriter
from typing import Generic, Iterable, TextIO, TypeVar
from os import PathLike

StrPath: TypeAlias = str | PathLike[str]


@dataclass
class Record(ABC):
    # def to_dict(self) -> dict[str, str]:
    #     raise NotImplementedError

    def to_dict(self) -> dict[str, str]:
        return {
            k: (v.value if isinstance((v := getattr(self, k)), Enum) else v)
            for k in self.__dataclass_fields__.keys()
        }

    @staticmethod
    def from_dict(record: dict[str, str]) -> "Record":
        raise NotImplementedError

    @staticmethod
    def parse_text_value(value: str | None) -> str | None:
        return value if value else None


T = TypeVar("T", bound=Record)


@dataclass
class RecordsFile(Iterable[T], Generic[T]):
    records: list[T]

    def __init__(self, records: list[T]) -> None:
        self.records = records

    def __iter__(self) -> Iterator[T]:
        return iter(self.records)

    def __next__(self) -> T:
        return next(self.__iter__())

    def to_dict_list(self) -> list[dict[str, str]]:
        return [record.to_dict() for record in self.records]

    def save(
        self,
        file: StrPath | TextIO,
    ) -> None:
        print("type of file:", type(file))
        print("is file string?", isinstance(file, str))
        if isinstance(file, str):
            with open(file, "w", newline="", encoding="utf-8-sig") as f:
                writer = DictWriter(
                    f, fieldnames=list(self.records[0].__dataclass_fields__)
                )
                writer.writeheader()
                writer.writerows(self.to_dict_list())
        elif isinstance(file, TextIOBase):
            writer = DictWriter(
                file, fieldnames=list(self.records[0].__dataclass_fields__)
            )
            writer.writeheader()
            writer.writerows(self.to_dict_list())
        else:
            raise ValueError("file must be a string or a file-like object")
