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
    }

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
        _links: dict = None,
        subject: str = None,
        description: str = None,
        schedule_manually: bool = None,
        readonly: bool = None,
        start_date: str = None,
        due_date: str = None,
        derived_start_date: str = None,
        derived_due_date: str = None,
        estimated_time: str = None,
        derived_estimated_time: str = None,
        percentage_done: int = None,
        custom_field_1: str = None,
        custom_field_2: str = None,
        created_at: str = None,
        updated_at: str = None,
        **kwargs,
    ):
        if _links is None and kwargs:
            _links = kwargs

        data = {
            self._args_api_mapping[k]: v
            for k, v in locals().items()
            if v is not None and k != "self" and k != "kwargs"
        }

        return self.client._send_request("POST", "/work_packages", data=data)

    def update(
        self,
        id: int,
        _links: dict = None,
        subject: str = None,
        description: str = None,
        schedule_manually: bool = None,
        readonly: bool = None,
        start_date: str = None,
        due_date: str = None,
        derived_start_date: str = None,
        derived_due_date: str = None,
        estimated_time: str = None,
        derived_estimated_time: str = None,
        percentage_done: int = None,
        custom_field_1: str = None,
        custom_field_2: str = None,
        created_at: str = None,
        updated_at: str = None,
        **kwargs,
    ):
        if _links is None and kwargs:
            _links = kwargs
        self._args_api_mapping["id"] = "id"
        data = {
            self._args_api_mapping[k]: v
            for k, v in locals().items()
            if v is not None and k != "self" and k != "kwargs"
        }
        data.pop("id")
        return self.client._send_request(
            "PATCH", f"/work_packages/{id}", data=data
        ).json()

    def delete(self, id: int):
        return self.client._send_request("DELETE", f"/work_packages/{id}")


client = Client(
    BASE_URL, "51de856c3f58f5eca1302305f7f34ce52f87c3224be4eb9c2af0314d29acbb1c"
)
work_packages = WorkPackages(client)
print(
    work_packages.update(
        id=1,
        subject="Test",
        project={"href": "/api/v3/projects/1"},
        type={"href": "/api/v3/types/1"},
        percentage_done=50,
    )
)
