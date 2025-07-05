class AppError(Exception):
    """Base class for known application exceptions."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class BadRequestError(AppError):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message, status_code=400)
