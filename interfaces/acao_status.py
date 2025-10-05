from abc import ABC, abstractmethod
from models.pedido import Pedido


class AcaoPosStatus(ABC):
    @abstractmethod
    def executar(self, pedido: Pedido):
        pass
