from dataclasses import dataclass, field
from typing import Generator, List, Type

from .. import Interface



@dataclass
class Stage:
    interface: Interface
    _data: dict
    base_url: str

    def __post_init__(self):
        self.hs_id = self._data.pop("id")
        self.base_url = f"{self.base_url}/stages/{self.hs_id}"
        self.__dict__.update(self._data)

    def __repr__(self):
        return f"<Pipeline Stage | {self.label}"


@dataclass
class Pipeline:
    interface: Interface
    _data: dict
    base_url: str

    def __repr__(self):
        return f"<Pipeline | {self.label}>"

    def __post_init__(self):
        self.hs_id: str = self._data.pop("id")
        self.base_url = f"{self.base_url}/{self.hs_id}"
        self.__dict__.update(self._data)
        self.stages: List["Stage"] = [Stage(self.interface, stage, self.base_url) for stage in self._data['stages']]


class PipelineFactory:
    def __init__(self, interface: Interface, base_url: str, api_version: int = 3):
        self.interface = interface
        self.api_version = api_version
        self.base_url = f"{base_url}/v{self.api_version}/pipelines"

    def get_all(self, hs_class: Type["HubSpotObject"]) -> Generator["Pipeline", None, None]:
        """
        Returns a Generator Pipeline Objects

        :return: Generator of Pipeline Objects
        """

        url = f"{self.base_url}/{hs_class.object_type}"
        response = self.interface.call(url)

        for result in response.json()["results"]:
            yield Pipeline(self.interface, result, url)
