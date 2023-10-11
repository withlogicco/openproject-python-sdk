class Error(Exception):
    """
    Base class for all API errors
    """

    def __init__(self, message, response=None):
        self.message = message
        self.response = response

    def __str__(self):
        return f"Error code {self.response.status_code}, Error message: {self.message}"


class AuthenticationError(Error):
    pass


class APIError(Error):
    pass
