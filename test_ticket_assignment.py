import pytest

from app.domain.errors import DuplicateAssignmentError
from app.models.entities import Ticket
from app.services.notifications import WebhookNotifier
from app.services.tickets import TicketService


class FakeTicketRepository:
    def __init__(self, tickets=None):
        self.tickets = tickets or {}
        self.updated = []

    def by_id(self, ticket_id):
        return self.tickets.get(ticket_id)

    def update(self, ticket):
        self.updated.append(ticket)
        self.tickets[ticket.id] = ticket


class FakeUserService:
    def __init__(self):
        self.users = {
            1: {"id": 1, "name": "Solicitante"},
            2: {"id": 2, "name": "Técnico"},
            3: {"id": 3, "name": "Otro técnico"},
        }

    def require(self, user_id):
        return self.users[user_id]


def test_no_permite_asignar_mismo_tecnico():
    ticket = Ticket(
        id=1,
        requester_id=1,
        assignee_id=2
    )

    ticket.history.append(
        {
            "action": "assigned",
            "technician_id": 2
        }
    )

    repository = FakeTicketRepository(
        {
            ticket.id: ticket
        }
    )

    users = FakeUserService()
    notifier = WebhookNotifier()

    service = TicketService(
        repository=repository,
        users=users,
        notifier=notifier
    )

    history_before = list(ticket.history)
    notifications_before = list(notifier.sent)
    updates_before = list(repository.updated)

    with pytest.raises(DuplicateAssignmentError):
        service.assign(
            ticket_id=1,
            technician_id=2
        )

    assert ticket.assignee_id == 2
    assert ticket.history == history_before
    assert notifier.sent == notifications_before
    assert repository.updated == updates_before


def test_webhook_notifier_registra_envio():
    notifier = WebhookNotifier()

    notifier.notify(
        "ticket_assigned",
        ticket_id=10,
        technician_id=5
    )

    assert len(notifier.sent) == 1

    assert notifier.sent[0]["args"] == (
        "ticket_assigned",
    )

    assert notifier.sent[0]["kwargs"] == {
        "ticket_id": 10,
        "technician_id": 5
    }


def test_asignacion_correcta():
    ticket = Ticket(
        id=1,
        requester_id=1,
        assignee_id=None
    )

    repository = FakeTicketRepository(
        {
            ticket.id: ticket
        }
    )

    users = FakeUserService()
    notifier = WebhookNotifier()

    service = TicketService(
        repository=repository,
        users=users,
        notifier=notifier
    )

    result = service.assign(
        ticket_id=1,
        technician_id=2
    )

    assert result.assignee_id == 2
    assert ticket.assignee_id == 2

    assert ticket.history == [
        {
            "action": "assigned",
            "technician_id": 2
        }
    ]

    assert len(repository.updated) == 1
    assert len(notifier.sent) == 1

