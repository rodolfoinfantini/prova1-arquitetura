from abc import ABC, abstractmethod


class INotificacaoService(ABC):
    @abstractmethod
    def enviar(self, destino: str, mensagem: str):
        pass
