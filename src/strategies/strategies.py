# strategies.py
from abc import ABC, abstractmethod
from utils.email_utils import send_email


class ResponseStrategy(ABC):
    @abstractmethod
    def execute(self, reclamo):
        pass

    @abstractmethod
    def get_content(self, reclamo):
        pass


class EmailResponseStrategy(ResponseStrategy):
    def execute(self, reclamo):
        send_email(
            str(reclamo.id_cliente),
            self.get_content(reclamo),
            "diegoalvarezmore@gmail.com",
        )

    def get_content(self, reclamo):
        return "Contenido específico del correo para la estrategia Email"


class LetterResponseStrategy(ResponseStrategy):
    def execute(self, reclamo):
        send_email(
            str(reclamo.id_cliente),
            self.get_content(reclamo),
            "diegoalvarezmore@gmail.com",
        )

    def get_content(self, reclamo):
        return "Contenido específico de la carta para la estrategia Letter"


class InPersonResponseStrategy(ResponseStrategy):
    def execute(self, reclamo):
        send_email(
            str(reclamo.id_cliente),
            self.get_content(reclamo),
            "diegoalvarezmore@gmail.com",
        )

    def get_content(self, reclamo):
        return "Contenido específico para respuesta presencial"
