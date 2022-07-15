import base64
from pathlib import Path
import json
from typing import BinaryIO, Union

from .File import File


class FileFactory:
    def __init__(self, interface):
        self.interface = interface
        self.base_url = "/files/v3/files"

    @staticmethod
    def _validate_options(access: str, ttl: str, overwrite: bool, dedup_strat: str, dedup_scope: str) -> str:
        errors = []
        options = dict()

        access_values = {"PRIVATE", "PUBLIC_INDEXABLE", "PUBLIC_NOT_INDEXABLE"}
        if access.upper() not in access_values:
            errors.append(f"access must be one of {access_values}")
        else:
            options.update({"access": access.upper()})

        if ttl is not None:
            options.update({"ttl": ttl})

        if overwrite is not None:
            options.update({"overwrite": overwrite})

        dedup_strat_values = {"REJECT", "RETURN_EXISTING", "NONE"}
        if dedup_strat is not None:
            if dedup_strat.upper() not in dedup_strat_values:
                errors.append(f"dedup_strat must be one of {dedup_strat_values}")
            else:
                options.update({"duplicateValidationStrategy": dedup_strat.upper()})

        dedup_scope_values = {"ENTIRE_PORTAL", "EXACT_FOLDER"}
        if dedup_scope is not None:
            if dedup_scope.upper() not in dedup_scope_values:
                errors.append(f"dedup_scope must be one of {dedup_scope_values}")
            else:
                options.update({"duplicateValidationScope": dedup_scope.upper()})

        if errors:
            raise Exception(" | ".join(errors))

        return json.dumps(options)

    def upload_file(self, file: Union[BinaryIO, Path], access: str, folder: Union[int, str],
                    file_name: str = None, charset_hunch: str = None,  ttl: str = None,
                    overwrite: bool = None, dedup_strat: str = None, dedup_scope: str = None) -> File:
        """
        Uploads a file to HubSpot and returns a File Object representing the uploaded file

        :param file: The Binary of the file to be uploaded or a pathlib.Path object representing the file
        :param access: Set the Access privs. Must be one of: PRIVATE, PUBLIC_INDEXABLE, PUBLIC_NOT_INDEXABLE
        :param folder: The folder to upload to.  Can be either path or folder id
        :param file_name: The name the file is to have once uploaded
        :param charset_hunch: Character set fo the uploaded file
        :param ttl: Sets retention time for the file
        :param overwrite: determines if the file will be over written
        :param dedup_strat: what happens if a duplicate is found.  Must be one of ENTIRE_PORTAL, EXACT_FOLDER, NONE
        :param dedup_scope: the scope of looking for duplicates. Must be one of REJECT, RETURN_EXISTING

        :return: a File Object representing the uploaded file
        """

        files = {
            "file": file.read_bytes() if isinstance(file, Path) else file,
            "fileName": file_name if file_name else file.name,
            "options": self._validate_options(access, ttl, overwrite, dedup_strat, dedup_scope)
        }

        if isinstance(folder, int):
            files.update({"folderId": folder})
        elif isinstance(folder, str):
            files.update({"folderPath": folder})

        if charset_hunch:
            files.update({"charsetHunch": charset_hunch})

        response = self.interface.call(self.base_url, method="POST", files=files)

        return File(self.interface, response.json())
