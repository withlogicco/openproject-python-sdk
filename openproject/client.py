import httpx


class Client:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url
        self.api_version = "v3"
        self.api_token = api_token

    def _handle_response(self, response: httpx.Response):
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")

        response.raise_for_status()
        return response.json()

    def _send_request(
        self, method: str, endpoint: str, params=None, data=None, **kwargs
    ) -> httpx.Response:
        url = f"{self.base_url}/api/{self.api_version}/{endpoint}"
        with httpx.Client(auth=("apikey", self.api_token)) as client:
            response = client.request(method, url, params=params, json=data, **kwargs)
            return self._handle_response(response)


class WorkPackages:
    def __init__(self, client: Client):
        self.client = client

    def list(self):
        return self.client._send_request("GET", "/work_packages")

    def view(self, id: int):
        return self.client._send_request("GET", f"/work_packages/{id}")

    def create(self, data: dict):
        return self.client._send_request("POST", "/work_packages", data=data)

    def update(self, id: int, data: dict):
        return self.client._send_request("PATCH", f"/work_packages/{id}", data=data)

    def delete(self, id: int):
        return self.client._send_request("DELETE", f"/work_packages/{id}")
