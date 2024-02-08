import httpx
from openproject.exceptions import APIError, AuthenticationError
from openproject.types import WorkPackage, Project
import json


class Client:
    """
    A client for interacting with the OpenProject API.
    """

    def __init__(self, base_url: str, api_token: str):
        """
        Initialize the client with the base URL and API token.
        """
        self.base_url = base_url
        self.api_version = "v3"
        self.api_token = api_token

        self.work_packages = WorkPackages(self)
        self.projects = Projects(self)
        self.statuses = Statuses(self)
        self.types = Types(self)

    def _handle_response(self, response: httpx.Response):
        """
        Handle the response from the API. Raises exceptions for error status codes.
        """
        if response.status_code == 401:
            error = response.json().get("message", "Authentication error")
            raise AuthenticationError(error, response.status_code)

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
                    error = f"Message: {error_message} , Error details: {resp.get('errors')}, {resp.get('data')}"
                    raise APIError(error, response)

            raise APIError(error, response)

    def _send_request(
        self, method: str, endpoint: str, params=None, data=None, **kwargs
    ) -> httpx.Response:
        """
        Send a request to the API and return the response.
        """
        url = f"{self.base_url}/api/{self.api_version}/{endpoint}"
        with httpx.Client(auth=("apikey", self.api_token)) as client:
            headers = {"Content-Type": "application/json"}
            response = client.request(
                method, url, params=params, json=data, headers=headers, **kwargs
            )
            return self._handle_response(response)


class SubClient(Client):
    client: Client

    def __init__(self, client: Client):
        self.client = client


class WorkPackages(SubClient):
    """
    A client for interacting with the WorkPackages endpoint of the OpenProject API.
    """

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

    def _api_payload_from_kwargs(self, **kwargs: WorkPackage):
        """
        Convert the keyword arguments to a dictionary that can be used as the payload in an API request.

        :param kwargs: The keyword arguments.
        :return: A dictionary that can be used as the payload in an API request.
        """
        items = self._args_api_mapping.items()
        data = {api_args: kwargs[args] for args, api_args in items if args in kwargs}
        return data

    def list(self, project: int | None):
        """
        List all work packages in a project.

        :param project: The ID of the project.
        :return: The response from the API.
        """
        params = {}
        if project:
            filters = [{"project": {"operator": "=", "values": project}}]
            params = {"filters": json.dumps(filters)}
        return self.client._send_request("GET", "work_packages", params=params)

    def view(self, id: int):
        """
        View a specific work package.

        :param id: The ID of the work package.
        :return: The response from the API.
        """
        return self.client._send_request("GET", f"work_packages/{id}")

    def create(self, **kwargs):
        """
        Create a new work package.

        :param kwargs: The properties of the work package.
        :return: The response from the API.
        """
        data = self._api_payload_from_kwargs(**kwargs)
        return self.client._send_request("POST", "work_packages", data=data)

    def update(self, id: int, **kwargs):
        """
        Update a specific work package.

        :param id: The ID of the work package.
        :param kwargs: The new properties of the work package.
        :return: The response from the API.
        """
        data = self._api_payload_from_kwargs(**kwargs)
        return self.client._send_request("PATCH", f"work_packages/{id}", data=data)

    def delete(self, id: int):
        """
        Delete a specific work package.

        :param id: The ID of the work package.
        :return: The response from the API.
        """
        return self.client._send_request("DELETE", f"work_packages/{id}")


class Projects(SubClient):
    """
    A client for interacting with the Projects endpoint of the OpenProject API.
    """

    _args_api_mapping = {
        "_links": "_links",
        "name": "name",
        "status_explanation": "statusExplanation",
        "description": "description",
    }

    def _api_payload_from_kwargs(self, **kwargs: Project):
        """
        Convert the keyword arguments to a dictionary that can be used as the payload in an API request.

        :param kwargs: The keyword arguments.
        :return: A dictionary that can be used as the payload in an API request.
        """
        items = self._args_api_mapping.items()
        data = {api_args: kwargs[args] for args, api_args in items if args in kwargs}
        return data

    def list(self):
        """
        List all projects.

        :return: The response from the API.
        """
        return self.client._send_request("GET", "projects")

    def view(self, id: int):
        """
        View a specific project.

        :param id: The ID of the project.
        :return: The response from the API.
        """
        return self.client._send_request("GET", f"projects/{id}")

    def create(self, **kwargs):
        """
        Create a new project.

        :param kwargs: The properties of the project.
        :return: The response from the API.
        """
        data = self._api_payload_from_kwargs(**kwargs)
        return self.client._send_request("POST", "projects", data=data)

    def update(self, id: int, **kwargs):
        """
        Update a specific project.

        :param id: The ID of the project.
        :param kwargs: The new properties of the project.
        :return: The response from the API.
        """
        data = self._api_payload_from_kwargs(**kwargs)
        return self.client._send_request("PATCH", f"projects/{id}", data=data)

    def delete(self, id: int):
        """
        Delete a specific project.

        :param id: The ID of the project.
        :return: The response from the API.
        """
        return self.client._send_request("DELETE", f"projects/{id}")

    def list_types(self, id: int):
        """
        List all types in a specific project.

        :param id: The ID of the project.
        :return: The response from the API.
        """
        return self.client._send_request("GET", f"projects/{id}/types")


class Statuses(SubClient):
    """
    A client for interacting with the Statuses endpoint of the OpenProject API.
    """

    def list(self):
        """
        List all statuses.

        :return: The response from the API.
        """
        return self.client._send_request("GET", "statuses")

    def view(self, id: int):
        """
        View a specific status.

        :param id: The ID of the status.
        :return: The response from the API.
        """
        return self.client._send_request("GET", f"statuses/{id}")


class Types(SubClient):
    """
    A client for interacting with the Types endpoint of the OpenProject API.
    """

    def list(self):
        """
        List all types.

        :return: The response from the API.
        """
        return self.client._send_request("GET", "types")

    def view(self, id: int):
        """
        View a specific type.

        :param id: The ID of the type.
        :return: The response from the API.
        """
        return self.client._send_request("GET", f"types/{id}")
