from typing import Any
import httpx

class BasicAuth(httpx.Auth):
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def auth_flow(self, request):
        auth_header = f"Basic {self._username}:{self._password}"
        request.headers["Authorization"] = auth_header
        yield request
