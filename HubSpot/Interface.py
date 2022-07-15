from requests import Session, Response


class Interface:

    def __init__(self, access_token: str, base_url: str):
        self.refresh_token = None
        self.auth_header = {"Authorization": f"Bearer {access_token}"}
        self.default_headers = {
            "Content-Type": "Application/JSON",
            **self.auth_header
        }
        self.session = Session()
        self.session.headers.update(self.default_headers)
        self.base_url = base_url

    def call(self, endpoint: str, method: str = "GET", **kwargs) -> Response:

        url = f"{self.base_url}{endpoint}"
        if "files" in kwargs.keys():
            content_type = self.session.headers = self.auth_header

        response = self.session.request(method=method, url=url, **kwargs)

        if "files" in kwargs.keys():
            self.session.headers.update(self.default_headers)

        response.raise_for_status()

        return response
