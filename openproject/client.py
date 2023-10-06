import httpx
from exceptions import APIError, AuthenticationError


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
            if method == "DELETE":
                headers = {"Content-Type": "application/hal+json"}
                response = client.request(
                    method, url, params=params, json=data, headers=headers, **kwargs
                )
                return self._handle_response(response)

            response = client.request(method, url, params=params, json=data, **kwargs)
            return self._handle_response(response)


class SubClient(Client):
    def __init__(self, client: Client):
        self.client = client


class WorkPackages(SubClient):
    def list(self):
        return self.client._send_request("GET", "/work_packages")

    def view(self, id: int):
        return self.client._send_request("GET", f"/work_packages/{id}")

    def _process_data(self, data):
        data = {
            k: v
            for k, v in data.items()
            if v is not None and k != "self" and k != "kwargs"
        }
        return data

    def create(
        self,
        _type: str = None,
        _links: dict = None,
        subject: str = None,
        description: str = None,
        scheduleManually: bool = None,
        readonly: bool = None,
        startDate: str = None,
        dueDate: str = None,
        derivedStartDate: str = None,
        derivedDueDate: str = None,
        estimatedTime: str = None,
        derivedEstimatedTime: str = None,
        percentageDone: int = None,
        customField1: str = None,
        customField2: str = None,
        createdAt: str = None,
        updatedAt: str = None,
        **kwargs,
    ):
        if _links is None and kwargs:
            _links = kwargs

        data = self._process_data(locals())
        return self.client._send_request("POST", "/work_packages", data=data)

    def update(
        self,
        id: int,
        _type: str = None,
        _links: dict = None,
        subject: str = None,
        description: str = None,
        scheduleManually: bool = None,
        readonly: bool = None,
        startDate: str = None,
        dueDate: str = None,
        derivedStartDate: str = None,
        derivedDueDate: str = None,
        estimatedTime: str = None,
        derivedEstimatedTime: str = None,
        percentageDone: int = None,
        customField1: str = None,
        customField2: str = None,
        createdAt: str = None,
        updatedAt: str = None,
        **kwargs,
    ):
        if _links is None and kwargs:
            _links = kwargs

        data = self._process_data(locals())
        data.pop("id")
        return self.client._send_request(
            "PATCH", f"/work_packages/{id}", data=data
        ).json()

    def delete(self, id: int):
        return self.client._send_request("DELETE", f"/work_packages/{id}")
