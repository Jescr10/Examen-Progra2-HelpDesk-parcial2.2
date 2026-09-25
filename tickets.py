from app.domain.errors import (
    TicketNotFoundError,
    DuplicateAssignmentError,
)


class TicketService:
    """
    Servicio encargado de las operaciones relacionadas con tickets.
    """

    def __init__(self, repository, users, notifier=None):
        # Las dependencias se reciben desde afuera.
        self._repository = repository
        self._users = users
        self._notifier = notifier

    def require(self, ticket_id: int):
        """
        Busca un ticket por su id.

        Si no existe, genera TicketNotFoundError.
        """
        ticket = self._repository.by_id(ticket_id)

        if ticket is None:
            raise TicketNotFoundError(
                f"No existe el ticket con id {ticket_id}."
            )

        return ticket

    def watchers(self, ticket_id: int) -> list:
        """
        Devuelve los usuarios relacionados con el ticket.

        Incluye:
        - Solicitante.
        - Técnico asignado, si existe.

        No devuelve usuarios duplicados.
        """
        ticket = self.require(ticket_id)

        user_ids = [ticket.requester_id]

        if (
            ticket.assignee_id is not None
            and ticket.assignee_id not in user_ids
        ):
            user_ids.append(ticket.assignee_id)

        return [
            self._users.require(user_id)
            for user_id in user_ids
        ]

    def assign(self, ticket_id: int, technician_id: int):
        """
        Asigna un técnico a un ticket.

        Impide asignar nuevamente al técnico que ya
        se encuentra asignado.
        """
        ticket = self.require(ticket_id)

        # Esta comprobación debe hacerse antes de modificar
        # historial o emitir notificaciones.
        if ticket.assignee_id == technician_id:
            raise DuplicateAssignmentError(
                f"El técnico {technician_id} ya está "
                f"asignado al ticket {ticket_id}."
            )

        # Comprueba que el técnico exista.
        technician = self._users.require(technician_id)

        # Asignación.
        ticket.assignee_id = technician_id

        # Registrar cambio en historial.
        ticket.history.append(
            {
                "action": "assigned",
                "technician_id": technician_id,
            }
        )

        # Comunicar el cambio al repositorio.
        self._repository.update(ticket)

        # Utiliza polimorfismo: TicketService no necesita
        # conocer qué clase concreta de Notifier está usando.
        if self._notifier is not None:
            self._notifier.notify(
                "ticket_assigned",
                ticket_id=ticket_id,
                technician_id=technician_id,
            )

        return ticket

