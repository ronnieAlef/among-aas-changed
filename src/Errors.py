class AmongAasException(Exception):
    def __init__(
            self,
            message: str,
            error_code: str,
            status_code: int = 400,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)


class InvalidInputException(AmongAasException):
    def __init__(self, item_id: int):

        super().__init__(
            message=f"Item {item_id} not found",
            error_code="item_not_found",
            status_code=404
        )


class InvalidUsernameException(AmongAasException):
    def __init__(self, username: str):

        super().__init__(
            message=f"{username} is invalid.",
            error_code="invalid username",
            status_code=409
        )


