from pathlib import Path
from typing import BinaryIO, Union

from .FileFactory import FileFactory
from .File import File


class Files:
    def __init__(self, interface):
        self.file_factory = FileFactory(interface)

    # HubSpot Files
    def upload(self, file: Union[BinaryIO, Path], access: str, folder: Union[str, int],
                    file_name: str = None, charset_hunch: str = None,  ttl: str = None,
                    overwrite: bool = None, dedup_strat: str = None, dedup_scope: str = None) -> File:
        """
        Uploads a file to HubSpot and returns a File Object representing the uploaded file

        :param file: The Binary of the file to be uploaded or a pathlib.Path object representing the file
        :param access: Set the Access privs. Must be one of: PRIVATE, PUBLIC_INDEXABLE, PUBLIC_NOT_INDEXABLE
        :param folder: The folder to upload the file to.  May be the path or folder id
        :param file_name: The name the file is to have once uploaded
        :param charset_hunch: Character set fo the uploaded file
        :param ttl: Sets retention time for the file
        :param overwrite: determines if the file will be over written
        :param dedup_strat: what happens if a duplicate is found.  Must be one of ENTIRE_PORTAL, EXACT_FOLDER, NONE
        :param dedup_scope: the scope of looking for duplicates. Must be one of REJECT, RETURN_EXISTING

        :return: a File Object representing the uploaded file
        """

        return self.file_factory.upload_file(file, access, folder, file_name, charset_hunch,
                                             ttl, overwrite, dedup_strat, dedup_scope)
