__all__ = [
    "ServiceError",
    "AuthenticationError",
    "NotFoundError",
    "DuplicateError",
    "ForbiddenError",
]


class ServiceError(Exception):
    def __init__(self, message, code) -> None:
        super().__init__(message, code)
        self.message = message
        self.code = code


class AuthenticationError(ServiceError):
    def __init__(self, message: str = "Invalid credentials.") -> None:
        super().__init__(message, 401)


class NotFoundError(ServiceError):
    def __init__(self, message: str = "Not found.") -> None:
        super().__init__(message, 404)


class ForbiddenError(ServiceError):
    def __init__(self) -> None:
        super().__init__("Forbidden.", 403)


class DuplicateError(ServiceError):
    def __init__(self, message: str = "Already exists.") -> None:
        super().__init__(message, 409)
