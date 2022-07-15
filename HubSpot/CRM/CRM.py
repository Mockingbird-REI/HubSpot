from typing import Dict, Generator, NoReturn, Type

from .HSObjects import HubSpotObject
from .Associations import Associations
from .HSFactory import HSFactory
from .Pipeline import Pipeline, PipelineFactory


class CRM:
    def __init__(self, interface):
        """
        :param access_token: App Access token
        """

        base_url = "/crm"
        self.association = Associations(interface, base_url)
        self.pipeline_factory = PipelineFactory(interface, base_url)
        self.hs_factory = HSFactory(interface, self.association, base_url)

    # HS Objects
    def list_objects(self, hs_class: Type[HubSpotObject], *args, **kwargs) -> Generator[Type[HubSpotObject], None, None]:
        for hs_object in self.hs_factory.list_all(hs_class, *args, **kwargs):
            yield hs_object

    def get_object(self, hs_class: Type[HubSpotObject], hs_id: int) -> HubSpotObject:
        return self.hs_factory.get(hs_class, hs_id)

    def new_object(self, hs_class: Type[HubSpotObject], **kwargs) -> HubSpotObject:
        return self.hs_factory.new(hs_class, **kwargs)

    def create_association(self, hs_obj_1: HubSpotObject, hs_obj_2: HubSpotObject, definer: str = "HUBSPOT_DEFINED",
                           association_type: int = None) -> NoReturn:
        """
        Associates 2 objects together in hubspot.

        :param hs_obj_1: one of the HubSpot Object to associate
        :param hs_obj_2: one of the HubSpot Object to associate
        :param definer: Who defined the association type? can be one of HUBSPOT_DEFINED, USER_DEFINED, or
                        INTEGRATOR_DEFINED
        :param association_type: The type of association to use.  Useful for custom Association Types or reverse the way
                                 companies are associated.

        :return: Associated Response

        Note: When linking a parent child relationship for companines, the first company will be considered the parent
            https://legacydocs.hubspot.com/docs/methods/crm-associations/crm-associations-overview
        """

        self.association.create_association(hs_obj_1, hs_obj_2, definer, association_type)

    def remove_association(self, hs_obj_1: HubSpotObject, hs_obj_2: HubSpotObject) -> NoReturn:
        """
        Removes the association between two objects in hubspot

        :param hs_obj_1: An object to remove association
        :param hs_obj_2: The other object involved in association removal

        :return: No Return
        """

        self.association.remove_association(hs_obj_1, hs_obj_2)

    def search(self, hs_class: Type[HubSpotObject], filters: Dict) -> Generator[HubSpotObject, None, None]:
        for hs_object in self.hs_factory.search(hs_class, filters):
            yield hs_object

    # HubSpot pipelines
    def list_pipelines(self, hs_class: Type[HubSpotObject]) -> Generator[Pipeline, None, None]:
        for pipeline in self.pipeline_factory.get_all(hs_class):
            yield pipeline
