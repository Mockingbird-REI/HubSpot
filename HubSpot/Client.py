from typing import List, Union
from .CRM import CRM, HubSpotObject, NOTE
from .Interface import Interface
from .Files import Files, File


class Client:
    def __init__(self, access_token: str, rate_limit: str = 10):
        """
        :param access_token: App Access token
        """

        interface = Interface(
            access_token=access_token,
            base_url="https://api.hubspot.com",
            rate_limit=rate_limit
        )
        self.crm = CRM(interface)
        self.files = Files(interface)

    def attach_file_crm(self, files: Union[List[File], File], crm_obj: HubSpotObject, time: int = None):
        """ Associates the file with the CRM Object.  Note, this is not for engagements

        :param files: the File to associate with the CRM Object
        :param crm_obj: The CRM object to associate the file with
        :param time: The time for the note to be attached to the object

        :return: the Note which facilitated the association

        Note: A note engagement is used to facilitate the association of the object and File.
        """

        if isinstance(files, File):
            attachment_ids = files.hs_id
        elif isinstance(files, list):
            attachment_ids = ";".join([file.hs_id for file in files])
        else:
            raise Exception("files must be a File or list of Files")

        params = {
            "hs_attachment_ids": attachment_ids
        }
        if time:
            params.update({"hs_timestamp": time})

        note = self.crm.new_object(NOTE, **params)

        note.associate(crm_obj)
