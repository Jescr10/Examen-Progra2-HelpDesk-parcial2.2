import pytest

from app.domain.errors import ValidationError
from app.models.entities import Ticket


def test_normalizacion_y_duplicados():
    ticket = Ticket(
        id=1,
        requester_id=10
    )

    ticket.add_tag(" Python ")
    ticket.add_tag("PYTHON")
    ticket.add_tag("python")

    assert ticket.tags == ("python",)


def test_rechaza_espacios_en_blanco():
    ticket = Ticket(
        id=1,
        requester_id=10
    )

    with pytest.raises(ValidationError):
        ticket.add_tag("     ")


def test_tags_independientes_entre_tickets():
    ticket1 = Ticket(
        id=1,
        requester_id=10
    )

    ticket2 = Ticket(
        id=2,
        requester_id=20
    )

    ticket1.add_tag("python")

    assert ticket1.tags == ("python",)
    assert ticket2.tags == ()


def test_tags_no_permite_reasignacion_publica():
    ticket = Ticket(
        id=1,
        requester_id=10
    )

    with pytest.raises(AttributeError):
        ticket.tags = ["java"]

