from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Union

from domain.exceptions.exception import InvalidStatusException

@dataclass(frozen=True)
class Ticket:
    """
    Business model representing a support ticket.

    Invariants:
    - A ticket always has an ID, a title, a description, a priority, a status, a date of creation, a date of update, a reporter and an assignee

    Transitions:
    - open() -> sets the ticket to Open status
    - start() -> sets the ticket to In Progress
    - close() -> sets the ticket to Closed
    - reopen() -> sets the ticket to Reopen
    - resolved() -> sets the ticket to Resolved
    """

    class Priority(Enum):
        LOW = "LOW"
        MEDIUM = "MEDIUM"
        HIGH = "HIGH"
        URGENT = "URGENT"

    class Status(Enum):
        OPEN = "OPEN"
        IN_PROGRESS = "IN PROGRESS"
        RESOLVED = "RESOLVED"
        CLOSED = "CLOSED"
        REOPENED = "REOPENED"

    _id: int
    _reporter_id: int
    _assignee_id: int
    _title: str
    _description: str
    _priority: Priority
    _status: Status
    _created_at: datetime
    _update_at: datetime
    

    # Immutable property
    @property
    def id(self) -> int: return self._id

    @property
    def reporter_id(self) -> int: return self._reporter_id

    @property
    def assignee_id(self) -> int: return self._assignee_id

    @property
    def title(self) -> str: return self._title

    @property
    def description(self) -> str: return self._description

    @property
    def priority(self) -> Priority: return self._priority

    @property
    def status(self) -> Status: return self._status

    @property
    def update_at(self) -> datetime: return self._update_at

    @property
    def created_at(self) -> datetime: return self._created_at

    # Explicit businness methods
    def open(self) -> Ticket: return self._replace(status=self.Status.OPEN)

    def start(self) -> Ticket:
        if self._status == self.Status.CLOSED:
            raise InvalidStatusException("Impssible de démarrer un ticket déjà fermé.")
        if self._status == self.Status.RESOLVED:
            raise InvalidStatusException("Impssible de démarrer un ticket déjà résolu.")
        return self._replace(status=self.Status.IN_PROGRESS)
    
    def close(self) -> Ticket:
        if self._status != self.Status.RESOLVED:
            raise InvalidStatusException("Impssible de fermer un ticket non résolu.")
        return self._replace(status=self.Status.CLOSED)
    
    def reopened(self) -> Ticket:
        if self._status != self.Status.CLOSED:
            raise InvalidStatusException("Impssible de reouvrir un ticket non fermé.")
        return self._replace(status=self.Status.REOPENED)
    
    def resolved(self) -> Ticket:
        if self._status != self.Status.IN_PROGRESS:
            raise InvalidStatusException("Impssible de résoudre un ticket non démarré.")
        return self._replace(status=self.Status.RESOLVED)
    
    # Internal method for creating a new modified instance
    def _replace(self, **changes: Union[int, str, Priority, Status, datetime]) -> "Ticket":
        data = self.__dict__.copy()
        data.update({f"_{k}": v for k, v in changes.items()})
        return Ticket(**data)
