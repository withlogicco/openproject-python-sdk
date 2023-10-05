import httpx
from exceptions import APIError, AuthenticationError
from constants import BASE_URL


class Client:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url
        self.api_version = "v3"
        self.api_token = api_token

    def _handle_response(self, response: httpx.Response):
        if response.status_code == 401:
            raise AuthenticationError(response.json()["message"], response.status_code)

        if response.status_code == 204:
            return None

        try:
            response.raise_for_status()

            return response.json()
        except:
            error = f"{response.text}"
            if "application/json" in response.headers["Content-Type"]:
                resp = response.json()
                if "message" in resp:
                    error = f"Message: {resp.get('message')} , Error details: {resp.get('errors')}, {resp.get('data')}"
                    raise APIError(error, response)

                elif "msg" in resp:
                    error = f"Message: {resp.get('msg')} , Error details: {resp.get('errors')}, {resp.get('data')}"
                    raise APIError(error, response)

            raise APIError(error, response)

    def _send_request(
        self, method: str, endpoint: str, params=None, data=None, **kwargs
    ) -> httpx.Response:
        url = f"{self.base_url}/api/{self.api_version}/{endpoint}"
        with httpx.Client(auth=("apikey", self.api_token)) as client:
            headers = {"Content-Type": "application/hal+json"}
            response = client.request(
                method, url, params=params, json=data, headers=headers, **kwargs
            )
            import pdb

            pdb.set_trace()
            return self._handle_response(response)


class SubClient(Client):
    def __init__(self, client: Client):
        self.client = client


class WorkPackages(SubClient):
    _args_api_mapping = {
        "project": "project",
        "type": "type",
        "subject": "subject",
    }

    def list(self):
        return self.client._send_request("GET", "/work_packages").json()

    def view(self, id: int):
        return self.client._send_request("GET", f"/work_packages/{id}").json()

    def create(self, project: dict, type: dict, subject: str):
        data = {
            self._args_api_mapping.get("project"): project,
            self._args_api_mapping.get("type"): type,
            self._args_api_mapping.get("subject"): subject,
        }
        return self.client._send_request("POST", "/work_packages", data=data).json()

    def update(self, id: int, project: dict, type: dict, subject: str, notify: bool):
        data = {
            self._args_api_mapping.get("project"): project,
            self._args_api_mapping.get("type"): type,
            self._args_api_mapping.get("subject"): subject,
            "notify": notify,
        }
        return self.client._send_request(
            "PATCH", f"/work_packages/{id}", data=data
        ).json()

    def delete(self, id: int):
        return self.client._send_request("DELETE", f"/work_packages/{id}").text
