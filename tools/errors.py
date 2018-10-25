class APIError(Exception):
    pass


class ResourceNotFoundError(APIError):
    pass


class InvalidCommandError(APIError):
    pass
