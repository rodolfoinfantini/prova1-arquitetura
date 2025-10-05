from abc import ABC, abstractmethod
from models.pedido import Pedido


class IPontosService(ABC):
    @abstractmethod
    def ganhar_pontos(self, pedido: Pedido):
        pass
