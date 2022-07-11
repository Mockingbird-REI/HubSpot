from datetime import datetime
import json
from typing import Dict, Generator, List, Union

from HubSpot import Interface
from . import HubSpotObject


class HSFactory:

    def __init__(self, interface: Interface, association):
        self.interface = interface
        self.association = association

    def list_all(self, hs_class: HubSpotObject.__class__, limit: int = 10, properties: List = None,
                 _after: Union[str, None] = None) -> Generator[HubSpotObject, None, None]:
        """
        Returns a list of the respective objects from Hubspot

        :param hs_class: The object type in question
        :param limit: The Number of results per page
        :param properties: The Properties to return for each object
        :param _after: The Next Page to query

        :return: A Generator of HubSpot Objects
        """

        endpoint = f"/v{hs_class.api_version}/objects/{hs_class.object_type}"
        params = {
            "limit": limit,
        }

        if _after is not None:
            params.update({"after": _after})

        if properties is not None:
            params.update({"properties": properties})

        response = self.interface.call(endpoint, params=params)
        response = response.json()

        for result in response["results"]:
            yield hs_class(self.interface, self.association, _data=result)

        if "after" in response:
            for result in self.list_all(hs_class, limit, properties, response["after"]):
                yield result

    def new(self, hs_class: HubSpotObject.__class__, **kwargs) -> HubSpotObject:
        """
        Creates a new object of this type in HubSpot

        :param hs_class: The object type in question
        :param kwargs: The Properties to create the object with

        :return: An object representing the newly created object in HubSpot
        """

        if "hs_timestamp" in hs_class.required_properties and "hs_timestamp" not in kwargs:
            kwargs.update({"hs_timestamp": str(datetime.utcnow()).replace(" ", "T") + "Z"})

        required_props = hs_class.required_properties.split(",")
        if required_props != [""] and not all([required_prop in kwargs for required_prop in required_props]):
            raise Exception(f"Missing Required Properties.  Required properties: {required_props}")

        endpoint = f"/v{hs_class.api_version}/objects/{hs_class.object_type}"
        data = json.dumps(
            {"properties": kwargs}
        )

        response = self.interface.call(endpoint, method="post", data=data)

        return hs_class(self.interface, self.association, response.json())

    def get(self, hs_class: HubSpotObject.__class__, hs_id: int) -> HubSpotObject:
        """
        Gets a singular HubSpot Object

        :param hs_class: The object type in question
        :param hs_id: the ID of the object to retrieve

        :return: an object representing the HS object
        """

        response = self.interface.call(f"{hs_class.endpoint}/{hs_id}")

        return hs_class(self.interface, self.association, response.json())

    def search(self, hs_class: HubSpotObject.__class__, filters: Dict, _after=None):
        """
        Searches Hubspot for the specified critieriea

        :param hs_class: The HubSpot Class we are looking for
        :param filters: The Filters for the HubSpot Class

        :return: a Generator of objects representing the filters HS Objects

        Filters should be in the format of FilterGroups[Filters].  See HubSpot for more information
        https://developers.hubspot.com/docs/api/crm/search#filter-search-results
        """

        url = f"/v{hs_class.api_version}/objects/{hs_class.object_type}/search"
        if _after is not None:
            filters.update({"after": _after})
        data = json.dumps(filters)

        response = self.interface.call(url, method="POST", data=data)
        data = response.json()
        for hs_data in data["results"]:
            yield hs_class(self.interface, self.association, hs_data)

        if "paging" in data:
            for result in self.search(hs_class, filters, data["paging"]["next"]["after"]):
                yield result
