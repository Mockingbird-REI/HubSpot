from requests import Session, Response


class Interface:

    def __init__(self, access_token: str, base_url: str):
        self.refresh_token = None
        self.session = Session()
        self.session.headers.update({
            "Content-Type": "Application/JSON",
            "Authorization": f"Bearer {access_token}"
        })
        self.base_url = base_url

    def call(self, endpoint: str, method: str = "GET", **kwargs) -> Response:

        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method=method, url=url, **kwargs)

        return response
