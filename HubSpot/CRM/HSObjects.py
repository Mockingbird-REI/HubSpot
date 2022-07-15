from dataclasses import dataclass, make_dataclass, field
import json
from typing import Dict, List, NoReturn, Any, ClassVar, Union

from ..Interface import Interface
from ..Files.File import File


@dataclass
class HubSpotObject:
    interface: Interface
    association: Any
    _data: Dict
    friendly_name: str
    required_properties: str = ""
    archived: bool = field(default=False)
    api_version: ClassVar[int] = 3
    object_type: ClassVar[str] = field(default=None)
    endpoint: str = f"/crm/v{api_version}/{object_type}"
    hs_id: int = field(init=False)

    def __post_init__(self):
        self.__dict__.update(self._data['properties'])
        self.archived = self._data['archived']
        self.hs_id = self._data['id']
        self.endpoint = f"/crm/v{self.api_version}/objects/{self.object_type}/{self.hs_id}"

    def __str__(self):
        return f"<{self.friendly_name} {self.hs_id}>"

    def update_hs(self, properties: Dict) -> NoReturn:
        """
        Updates the object in HubSpot with the given properties, and the local
        object is updated inplace.

        :param properties: The properties to update

        :return: NoReturn
        """

        data = json.dumps(properties)
        response = self.interface.call(self.endpoint, method="put", data=data)

        self.__dict__.update(response.json()["properties"])

    def archive(self) -> NoReturn:
        """
        Archives the object in hubspot, and archived is set to true in local object

        :return: No Return
        """

        response = self.interface.call(self.endpoint, method="delete")

        self.archived = True

    def associate(self, hs_object: Union["HubSpotObject", File], *args, **kwargs) -> NoReturn:
        """
        Creates an association from this object to the hs_object

        :param hs_object: The object to associate with this object

        :return: No Return

        See Associations.create_association for more arguments
        """

        self.association.create_association(self, hs_object, *args, **kwargs)

    def remove_association(self, hs_object: "HubSpotObject") -> NoReturn:
        """
        Removes the association of this object to the defined object

        :param hs_object: the object to remove the association from

        :return: NoReturn
        """

        self.association.remove_association(self, hs_object)


def _not_implemented(*args, **kwargs):
    pass


# HS Objects
COMPANY = make_dataclass("Company",
                         [("friendly_name", str, field(default="Company")),
                          ("object_type", ClassVar[str], "companies")],
                         bases=(HubSpotObject, ))


CONTACT = make_dataclass("Contact",
                         [("friendly_name", str, field(default="Contact")),
                          ("object_type", ClassVar[str], "contacts")],
                         bases=(HubSpotObject, ))


DEAL = make_dataclass("Deal",
                      [("friendly_name", str, "Deal"),
                       ("object_type", ClassVar[str], "deals")],
                      bases=(HubSpotObject, ))


FEEDBACK_SUBMISSION = make_dataclass("FeedbackSubmission",
                                     [("friendly_name", str, field(default="Feedback Submission")),
                                      ("object_type", str, "companies")],
                                     bases=(HubSpotObject, ),
                                     namespace={
                                         "new": _not_implemented(),
                                         "update_hs": _not_implemented()
                                     })


LINE_ITEM = make_dataclass("LineItem",
                           [("friendly_name", str, field(default="Line Item")),
                            ("object_type", str, "line_items")],
                           bases=(HubSpotObject, ))


PRODUCT = make_dataclass("Product",
                         [("friendly_name", str, field(default="Product")),
                          ("object_type", str, "products")],
                         bases=(HubSpotObject, ))


TICKET = make_dataclass("Ticket",
                        [("friendly_name", str, field(default="Ticket")),
                         ("object_type", str, "tickets"),
                         ("required_properties", str, field(default="hs_pipeline_stage"))],
                        bases=(HubSpotObject, ))

# HS Engagements

_hs_engagement = make_dataclass("HS_ENGAGEMENT",
                                [("api_version", int, field(default=4)),
                                 ("required_properties", str, "hs_timestamp")],
                                bases=(HubSpotObject, ))

CALL = make_dataclass("Call",
                      [("friendly_name", str, field(default="Call")),
                       ("object_type", str, "calls")],
                      bases=(_hs_engagement, ))


EMAIL = make_dataclass("Email",
                       [("friendly_name", str, field(default="email")),
                        ("object_type", str, "emails")],
                       bases=(_hs_engagement, ))


MEETING = make_dataclass("Meeting",
                         [("friendly_name", str, field(default="Meeting")),
                          ("object_type", str, "meetings")],
                         bases=(_hs_engagement, ))


NOTE = make_dataclass("Note",
                      [("friendly_name", str, field(default="Note")),
                       ("object_type", str, "notes")],
                      bases=(_hs_engagement, ))


TASK = make_dataclass("Task",
                      [("friendly_name", str, field(default="Task")),
                       ("object_type", str, "tasks")],
                      bases=(_hs_engagement, ))

ASSOCIATION_MATRIX = (
        (CONTACT, COMPANY),
        (COMPANY, CONTACT),
        (DEAL, CONTACT),
        (CONTACT, DEAL),
        (DEAL, COMPANY),
        (COMPANY, DEAL),
        (COMPANY, _hs_engagement),
        (_hs_engagement, COMPANY),
        (CONTACT, _hs_engagement),
        (_hs_engagement, CONTACT),
        (DEAL, _hs_engagement),
        (_hs_engagement, DEAL),
        (COMPANY, COMPANY),
        (COMPANY, COMPANY),
        (CONTACT, TICKET),
        (TICKET, CONTACT),
        (TICKET, _hs_engagement),
        (_hs_engagement, TICKET),
        (DEAL, LINE_ITEM),
        (LINE_ITEM, DEAL),
        (None, None),
        (None, None),
        (None, None),
        (None, None),
        (COMPANY, TICKET),
        (TICKET, COMPANY),
        (DEAL, TICKET),
        (TICKET, DEAL)
)