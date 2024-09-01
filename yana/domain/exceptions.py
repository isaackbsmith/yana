class DatabaseError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail

class QueryError(Exception):
    def __init__(self,
                 detail: str = "A Query Error Occurred") -> None:
        self.detail = detail

class ServiceError(Exception):
    def __init__(self,
                 detail: str = "A service Error Occurred") -> None:
        self.detail = detail
