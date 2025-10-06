class AppError(Exception):
    code: int = 500
    message: str = "Internal Server Error"

    def __init__(
        self, message: str | None = None, code: int | None = None, *args: object
    ) -> None:
        self.message = message or self.message
        self.code = code or self.code

        super().__init__(self.message, *args)
