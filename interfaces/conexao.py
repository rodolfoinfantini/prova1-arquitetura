from abc import ABC, abstractmethod


class IConexao(ABC):
    @abstractmethod
    def get_conexao(self):
        pass
