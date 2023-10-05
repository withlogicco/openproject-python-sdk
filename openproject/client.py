import httpx


class Client:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url
        self.api_version = "v3"
        self.api_token = api_token

    def _handle_response(self, response: httpx.Response) -> httpx.Response:
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")

        response.raise_for_status()
        return response

    def _send_request(
        self, method: str, url: str, params=None, data=None, **kwargs
    ) -> httpx.Response:
        with httpx.Client(auth=("apikey", self.api_token)) as client:
            response = client.request(method, url, params=params, json=data, **kwargs)
            return self._handle_response(response)


class WorkPackages:
    def __init__(self, client: Client):
        self.client = client

    def list(self):
        url = f"{self.client.base_url}/api/{self.client.api_version}/work_packages"
        response = self.client._send_request("GET", url)
        return response.json()
