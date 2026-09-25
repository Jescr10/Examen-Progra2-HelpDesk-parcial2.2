# Segundo Parcial - Programación II
## Proyecto HelpDesk EDU

Este proyecto contiene la resolución de los ejercicios prácticos correspondientes al segundo parcial de Programación II.

## Ejercicio 1 - Etiquetas y encapsulamiento

Se agregó a la entidad `Ticket` una colección interna `_tags`.

Características implementadas:

- Uso de `field(default_factory=list, init=False, repr=False)`.
- Propiedad pública `tags` de solo lectura.
- Conversión de la lista interna a `tuple`.
- Método `add_tag(tag)`.
- Normalización mediante `strip()` y `lower()`.
- Rechazo de etiquetas vacías mediante `ValidationError`.
- Prevención de etiquetas duplicadas.
- Independencia de etiquetas entre diferentes tickets.
- Reasignación pública de `tags` bloqueada.

### Pruebas realizadas

- Normalización de etiquetas.
- Eliminación de duplicados.
- Rechazo de espacios en blanco.
- Independencia entre dos tickets.
- Rechazo de reasignación pública.

---

## Ejercicio 2 - Observadores y relaciones entre objetos

Se agregó el método:

```python
watchers(ticket_id)
```

Este método:

- Obtiene el ticket mediante `self.require(ticket_id)`.
- Incluye al solicitante del ticket.
- Incluye al técnico asignado cuando existe.
- Evita devolver usuarios duplicados.
- Obtiene los usuarios mediante `self._users.require(id)`.
- No accede directamente al repositorio de usuarios.

### Pruebas realizadas

- Ticket sin técnico asignado.
- Ticket con solicitante y técnico diferentes.
- Eliminación de usuarios duplicados.
- Propagación de `TicketNotFoundError` cuando el ticket no existe.

---

## Ejercicio 3 - Excepciones y polimorfismo

Se agregó la excepción:

```python
DuplicateAssignmentError
```

como subclase de `DomainError`.

El método `assign()` rechaza la asignación cuando el técnico indicado ya se encuentra asignado al ticket.

La validación se ejecuta antes de:

- Modificar el historial.
- Actualizar el repositorio.
- Emitir notificaciones.

También se implementó:

```python
WebhookNotifier
```

como implementación del contrato `Notifier`.

`WebhookNotifier` simula el envío de un webhook almacenando en memoria los argumentos recibidos, sin realizar llamadas HTTP reales.

### Pruebas realizadas

- Reasignación del mismo técnico genera `DuplicateAssignmentError`.
- El historial no cambia cuando ocurre la excepción.
- No se registra una notificación cuando ocurre la excepción.
- No se actualiza el repositorio cuando ocurre la excepción.
- Una asignación válida actualiza correctamente el ticket.
- `WebhookNotifier` registra correctamente sus argumentos.

---

## Ejercicio 4 - SQL e integridad referencial

Las consultas correspondientes se encuentran en:

```text
docs/database/queries_parcial2.sql
```

Se incluyen las siguientes consultas:

1. Tickets abiertos junto con el nombre del solicitante mediante `JOIN`.
2. Conteo de tickets por técnico asignado utilizando `GROUP BY` y `HAVING`.
3. Tickets sin comentarios mediante `NOT EXISTS`.
4. Demostración de `ON DELETE CASCADE` mediante `BEGIN`, `DELETE` y `ROLLBACK`.

La prueba de cascada debe demostrar:

- Un conteo inicial del historial mayor que cero.
- Conteo igual a cero después de eliminar temporalmente el ticket.
- Recuperación del conteo original después de ejecutar `ROLLBACK`.

---

## Ejercicio 5 - Consulta agregada con SQLAlchemy

Se implementa en `SqlAlchemyTicketRepository` el método:

```python
count_by_status() -> dict[str, int]
```

El método obtiene el número de tickets agrupados por estado utilizando SQLAlchemy.

La consulta utiliza:

```python
select(
    TicketORM.status,
    func.count()
).group_by(TicketORM.status)
```

Las pruebas utilizan SQLite en memoria y `StaticPool`.

Se debe comprobar:

- Dos tickets en un estado.
- Un ticket en otro estado.
- Un total de tres tickets.
- Persistencia después de `commit()`.
- Consulta desde una nueva sesión.
- Resultado vacío en una base de datos independiente sin tickets.

---

## Ejecución de pruebas

Desde la carpeta raíz del proyecto ejecutar:

```bash
py -m pytest -q
```

Resultado obtenido inicialmente para los ejercicios 1, 2 y 3:

```text
11 passed
```

Los ejercicios 4 y 5 deben agregarse posteriormente a la evidencia final.

---

## Estructura principal del proyecto

```text
HelpdeskEDU_P2/
│
├── app/
│   ├── domain/
│   │   └── errors.py
│   │
│   ├── models/
│   │   └── entities.py
│   │
│   ├── repositories/
│   │   └── sqlalchemy.py
│   │
│   └── services/
│       ├── notifications.py
│       └── tickets.py
│
├── docs/
│   └── database/
│       └── queries_parcial2.sql
│
├── test/
│   ├── test_ticket_assignment.py
│   ├── test_ticket_tags.py
│   ├── test_ticket_watchers.py
│   └── test_count_by_status.py
│
└── README_parcial2.md
```

---

## Control de versiones

Cada ejercicio se trabaja en una rama independiente y posteriormente se integra a `Main`.

Ramas utilizadas:

```text
Feature_etiquetasEncapsuladas
Feature_observadores
Feature_excepcionesPolimorfismo
Feature_sqlIntegridadReferencial
Feature_countByStatus
```

Cada feature debe contener sus respectivos commits antes de realizar el merge a `Main`.

---

## Resultado

El proyecto implementa encapsulamiento, validaciones de dominio, relaciones entre objetos, excepciones personalizadas, polimorfismo, pruebas automatizadas, consultas SQL, integridad referencial y consultas agregadas mediante SQLAlchemy.
