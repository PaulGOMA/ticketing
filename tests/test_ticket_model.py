import pytest
from datetime import datetime
from dataclasses import FrozenInstanceError

from src.domain.exceptions.exception import InvalidStatusException
from src.domain.model.ticket import Ticket


# --- FIXTURES -----------------------------------------------------------------

@pytest.fixture
def fixed_dates():
    now = datetime.now()
    return now, now


@pytest.fixture
def base_ticket(fixed_dates: tuple[datetime, datetime]):
    created_at, updated_at = fixed_dates
    return Ticket(
        1,
        2,
        3,
        "Problème de connexion",
        "Impossible de se connecter au VPN",
        Ticket.Priority.HIGH,
        Ticket.Status.OPEN,
        created_at,
        updated_at,
    )


# --- TESTS INVARIANTS ---------------------------------------------------------

class TestTicketInvariants:

    def test_ticket_fields_are_correct(self, base_ticket: Ticket, fixed_dates: tuple[datetime, datetime]):
        created_at, updated_at = fixed_dates

        assert base_ticket.id == 1
        assert base_ticket.reporter_id == 2
        assert base_ticket.assignee_id == 3
        assert base_ticket.title == "Problème de connexion"
        assert base_ticket.description == "Impossible de se connecter au VPN"
        assert base_ticket.priority == Ticket.Priority.HIGH
        assert base_ticket.status == Ticket.Status.OPEN
        assert base_ticket.created_at == created_at
        assert base_ticket.update_at == updated_at

    def test_ticket_is_immutable(self, base_ticket: Ticket):
        with pytest.raises(FrozenInstanceError):
            base_ticket.id = 99 # type: ignore


# --- TESTS TRANSITIONS --------------------------------------------------------

class TestTicketTransitions:

    def test_close_from_open_raises(self, base_ticket: Ticket):
        with pytest.raises(InvalidStatusException) as e:
            base_ticket.close()

        assert "Impossible de fermer un ticket non résolu." in str(e.value)

    def test_reopen_from_open_raises(self, base_ticket: Ticket):
        with pytest.raises(InvalidStatusException) as e:
            base_ticket.reopened()

        assert "Impossible de reouvrir un ticket non fermé." in str(e.value)

    def test_valid_transition_flow(self, base_ticket: Ticket):
        # OPEN → IN_PROGRESS
        t1 = base_ticket.start()
        assert t1.status == Ticket.Status.IN_PROGRESS

        # IN_PROGRESS → RESOLVED
        t2 = t1.resolved()
        assert t2.status == Ticket.Status.RESOLVED

        # RESOLVED → CLOSED
        t3 = t2.close()
        assert t3.status == Ticket.Status.CLOSED

        # CLOSED → REOPENED
        t4 = t3.reopened()
        assert t4.status == Ticket.Status.REOPENED
