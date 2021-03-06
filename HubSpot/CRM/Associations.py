import json
from typing import NoReturn, Union

from .HSObjects import ASSOCIATION_MATRIX, _hs_engagement
from ..Interface import Interface
from ..Files.File import File
from .HSObjects import HubSpotObject


class Associations:
    def __init__(self, interface: Interface, base_url: str):
        self.interface = interface
        self.base_url = base_url

    @staticmethod
    def _association_class(hs_object):
        if isinstance(hs_object, _hs_engagement) or isinstance(hs_object, File):
            return _hs_engagement

        return hs_object.__class__

    def create_association(self, hs_obj_1: Union[HubSpotObject, File], hs_obj_2: Union[HubSpotObject, File],
                           definer: str = "HUBSPOT_DEFINED", association_type: int = None) -> NoReturn:
        """
        Associates 2 objects together in hubspot.

        :param hs_obj_1: one of the HubSpot Object or File to associate
        :param hs_obj_2: one of the HubSpot Object or File to associate
        :param definer: Who defined the association type? can be one of HUBSPOT_DEFINED, USER_DEFINED, or
                        INTEGRATOR_DEFINED
        :param association_type: The type of association to use.  Useful for custom Association Types or reverse the way
                                 companies are associated.

        :return: Associated Response

        Note: When linking a parent child relationship for companies, the first company will be considered the parent
            https://legacydocs.hubspot.com/docs/methods/crm-associations/crm-associations-overview
        """

        definer = definer.upper()
        if definer not in ("HUBSPOT_DEFINED", "USER_DEFINED", "INTEGRATOR_DEFINED"):
            raise Exception("bad definer")

        association_type_ids = list(range(1, 29))
        for bad_association_id in {21, 22, 23, 24}:
            association_type_ids.pop(bad_association_id)

        hubspot_defined_conditions = (
            definer == "HUBSPOT_DEFINED",
            association_type is not None,
            association_type not in association_type_ids
        )
        if all(hubspot_defined_conditions):
            raise Exception("Can not use non hubspot defined association types with definer HUBSPOT_DEFINED")

        if association_type is None and definer == "HUBSPOT_DEFINED":
            association = (self._association_class(hs_obj_1),
                           self._association_class(hs_obj_2))
            association_type = ASSOCIATION_MATRIX.index(association)
            association_type += 1

        url = (f"{self.base_url}/v4/objects/{getattr(hs_obj_1, 'object_type', 'files')}/{hs_obj_1.hs_id}"
               f"/associations/{getattr(hs_obj_2, 'object_type', 'files')}/{hs_obj_2.hs_id}")
        data = json.dumps([{
            "associationCategory": definer,
            "associationTypeId": association_type
        }])

        response = self.interface.call(url, method="put", data=data)

        return response.json()

    def remove_association(self, hs_obj_1: Union[HubSpotObject, File], hs_obj_2: Union[HubSpotObject, File]
                           ) -> NoReturn:
        """
        Removes the association between two objects in hubspot

        :param hs_obj_1: An object to remove association
        :param hs_obj_2: The other object involved in association removal

        :return: No Return
        """

        url = (f"{self.base_url}/v4/objects/{hs_obj_1.object_type}/{hs_obj_1.hs_id}"
               f"/associations/{hs_obj_2.object_type}/{hs_obj_2.hs_id}")

        response = self.interface.call(url, method="delete")
