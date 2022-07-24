import logging
from requests import Session, Response
from time import sleep


class Interface:

    def __init__(self, access_token: str, base_url: str, rate_limit=10):
        self.refresh_token = None
        self.auth_header = {"Authorization": f"Bearer {access_token}"}
        self.default_headers = {
            "Content-Type": "Application/JSON",
            **self.auth_header
        }
        self.session = Session()
        self.session.headers.update(self.default_headers)
        self.base_url = base_url
        self.rate_limit = rate_limit

    def call(self, endpoint: str, method: str = "GET", **kwargs) -> Response:
        logging.debug(f"callling ({method}) {endpoint}")
        sleep(1)

        url = f"{self.base_url}{endpoint}"
        if "files" in kwargs.keys():
            content_type = self.session.headers = self.auth_header

        response = self.session.request(method=method, url=url, **kwargs)

        if "files" in kwargs.keys():
            self.session.headers.update(self.default_headers)

        try:
            response.raise_for_status()
        except Exception as e:
            try:
                print(response.json())
            except:
                pass

            raise e

        return response
