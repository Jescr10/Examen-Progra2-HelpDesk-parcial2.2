from abc import ABC, abstractmethod


class Notifier(ABC):
    """
    Contrato base para los notificadores del sistema.
    """

    @abstractmethod
    def notify(self, *args, **kwargs):
        """
        Envía o registra una notificación.
        """
        pass


class WebhookNotifier(Notifier):
    """
    Simula un webhook sin realizar peticiones HTTP.

    Guarda los argumentos recibidos en memoria para
    poder verificarlos durante las pruebas.
    """

    def __init__(self):
        self.sent = []

    def notify(self, *args, **kwargs):
        self.sent.append(
            {
                "args": args,
                "kwargs": kwargs,
            }
        )

