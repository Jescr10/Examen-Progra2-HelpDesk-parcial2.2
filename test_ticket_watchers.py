from dataclasses import dataclass

import pytest

from app.domain.errors import TicketNotFoundError
from app.models.entities import Ticket
from app.services.tickets import TicketService


@dataclass
class FakeUser:
    id: int
    name: str


class FakeTicketRepository:
    def __init__(self, tickets=None):
        self.tickets = tickets or {}

    def by_id(self, ticket_id):
        return self.tickets.get(ticket_id)

    def update(self, ticket):
        self.tickets[ticket.id] = ticket


class FakeUserService:
    def __init__(self):
        self.users = {
            1: FakeUser(
                id=1,
                name="Solicitante"
            ),
            2: FakeUser(
                id=2,
                name="Técnico"
            ),
        }

    def require(self, user_id):
        return self.users[user_id]


def test_watchers_sin_tecnico():
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

    service = TicketService(
        repository=repository,
        users=users
    )

    watchers = service.watchers(ticket.id)

    assert len(watchers) == 1
    assert watchers[0].id == 1


def test_watchers_con_tecnico():
    ticket = Ticket(
        id=1,
        requester_id=1,
        assignee_id=2
    )

    repository = FakeTicketRepository(
        {
            ticket.id: ticket
        }
    )

    users = FakeUserService()

    service = TicketService(
        repository=repository,
        users=users
    )

    watchers = service.watchers(ticket.id)

    assert len(watchers) == 2

    assert {
        user.id
        for user in watchers
    } == {1, 2}


def test_watchers_no_duplica_usuario():
    ticket = Ticket(
        id=1,
        requester_id=1,
        assignee_id=1
    )

    repository = FakeTicketRepository(
        {
            ticket.id: ticket
        }
    )

    users = FakeUserService()

    service = TicketService(
        repository=repository,
        users=users
    )

    watchers = service.watchers(ticket.id)

    assert len(watchers) == 1
    assert watchers[0].id == 1


def test_watchers_propaga_error_ticket_inexistente():
    repository = FakeTicketRepository()
    users = FakeUserService()

    service = TicketService(
        repository=repository,
        users=users
    )

    with pytest.raises(TicketNotFoundError):
        service.watchers(99999)
