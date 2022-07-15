from dataclasses import dataclass
import json
from pathlib import Path
from typing import BinaryIO, Union

from HubSpot import Interface


@dataclass
class File:
    interface: Interface
    _data: dict

    def __post_init__(self):
        self.hs_id: str = self._data.pop("id")
        self.__dict__.update(self._data)

    def __repr__(self):
        return f"<File {self.name} {self.type}>"

