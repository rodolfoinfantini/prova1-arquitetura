from abc import ABC, abstractmethod


class IRelatorioService(ABC):
    @abstractmethod
    def gerar_relatorio(self):
        pass
