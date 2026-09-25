class DomainError(Exception):
    """Excepción base para errores del dominio."""
    pass


class NotFoundError(DomainError):
    """Error base cuando una entidad no existe."""
    pass


class TicketNotFoundError(NotFoundError):
    """Se genera cuando un ticket no existe."""
    pass


class UserNotFoundError(NotFoundError):
    """Se genera cuando un usuario no existe."""
    pass


class ValidationError(DomainError):
    """Se genera cuando un dato del dominio no es válido."""
    pass


class DuplicateAssignmentError(DomainError):
    """Se genera al intentar asignar nuevamente el mismo técnico."""
    pass
