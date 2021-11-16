from vektonn.dtos import ErrorDto


class VektonnApiError(BaseException):
    def __init__(
        self,
        status: int,
        error: ErrorDto,
    ):
        self.status = status
        self.error = error
        super().__init__()
