from typing import Optional

from vektonn.dtos import ErrorDto


class VektonnError(Exception):
    def __init__(
        self,
        message: str,
        inner_exception: Optional[Exception] = None
    ):
        if inner_exception is not None:
            message = f'{message}\nInnerException: {repr(inner_exception)}'
        super().__init__(message)


class VektonnApiError(VektonnError):
    def __init__(
        self,
        status: int,
        error: Optional[ErrorDto],
    ):
        self.status = status
        self.error = error
        message = f'Status: {status}. ErrorMessages: {"; ".join(error.error_messages) if error is not None else "None"}'
        super().__init__(message)
