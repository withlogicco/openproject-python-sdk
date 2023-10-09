import httpx
from exceptions import APIError, AuthenticationError
from openproject.types import WorkPackage


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
            content_type = response.headers.get("Content-Type", "").lower()
            if content_type == "application/json":
                resp = response.json()
                error_message_keys = ("message", "msg")
                error_message = next(
                    (resp[key] for key in error_message_keys if key in resp), None
                )
                if error_message:
                    error = f"Message: {resp.get('message')} , Error details: {resp.get('errors')}, {resp.get('data')}"
                    raise APIError(error, response)

            raise APIError(error, response)

    def _send_request(
        self, method: str, endpoint: str, params=None, data=None, **kwargs
    ) -> httpx.Response:
        url = f"{self.base_url}/api/{self.api_version}/{endpoint}"
        with httpx.Client(auth=("apikey", self.api_token)) as client:
            headers = {"Content-Type": "application/json"}
            response = client.request(
                method, url, params=params, json=data, headers=headers, **kwargs
            )
            return self._handle_response(response)


class SubClient(Client):
    def __init__(self, client: Client):
        self.client = client


class WorkPackages(SubClient):
    _args_api_mapping = {
        "_links": "_links",
        "subject": "subject",
        "description": "description",
        "schedule_manually": "scheduleManually",
        "readonly": "readonly",
        "start_date": "startDate",
        "due_date": "dueDate",
        "derived_start_date": "derivedStartDate",
        "derived_due_date": "derivedDueDate",
        "estimated_time": "estimatedTime",
        "derived_estimated_time": "derivedEstimatedTime",
        "percentage_done": "percentageDone",
        "custom_field_1": "customField1",
        "custom_field_2": "customField2",
        "created_at": "createdAt",
        "updated_at": "updatedAt",
        "lock_version": "lockVersion",
    }

    def _api_payload_from_kwargs(self, **kwargs) -> WorkPackage:
        data = {}
        for arg, api_arg in self._args_api_mapping.items():
            if arg in kwargs:
                data[api_arg] = kwargs[arg]
        return data

    def list(self):
        return self.client._send_request("GET", "/work_packages")

    def view(self, id: int):
        return self.client._send_request("GET", f"/work_packages/{id}")

    def create(self, **kwargs):
        data = self._api_payload_from_kwargs(**kwargs)
        return self.client._send_request("POST", "/work_packages", data=data)

    def update(self, id: int, **kwargs):
        data = self._api_payload_from_kwargs(**kwargs)
        return self.client._send_request("PATCH", f"/work_packages/{id}", data=data)

    def delete(self, id: int):
        return self.client._send_request("DELETE", f"/work_packages/{id}")
