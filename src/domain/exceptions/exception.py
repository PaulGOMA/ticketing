class InvalidStatusException(Exception):
    """Exception triggered when the ticket status is wrong"""
    def __init__(self, message: str) -> None:
        super().__init__(message)