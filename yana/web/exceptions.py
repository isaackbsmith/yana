from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, item: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item} Not Found")


class ValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation Error: {detail}")


class InternalServerError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An Internal Server Error Occurred")



