from dataclasses import dataclass, field

from app.domain.errors import ValidationError


@dataclass
class Ticket:
    """
    Entidad de dominio que representa un ticket del sistema HelpDesk.
    """

    id: int
    requester_id: int
    assignee_id: int | None = None
    status: str = "open"

    # Historial independiente para cada ticket.
    history: list = field(default_factory=list)

    # Lista interna protegida de etiquetas.
    _tags: list[str] = field(
        default_factory=list,
        init=False,
        repr=False
    )

    @property
    def tags(self) -> tuple[str, ...]:
        """
        Devuelve las etiquetas como una colección de solo lectura.
        """
        return tuple(self._tags)

    def add_tag(self, tag: str) -> None:
        """
        Agrega una etiqueta normalizada.

        - Elimina espacios externos.
        - Convierte a minúsculas.
        - Rechaza valores vacíos.
        - Evita etiquetas duplicadas.
        """
        normalized_tag = tag.strip().lower()

        if not normalized_tag:
            raise ValidationError(
                "La etiqueta no puede estar vacía."
            )

        if normalized_tag not in self._tags:
            self._tags.append(normalized_tag)

