from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
TId = TypeVar("TId")


class Repository(ABC, Generic[T, TId]):
    @abstractmethod
    def salvar(self, dados: T) -> T:
        pass

    @abstractmethod
    def recuperar_tudo(self) -> list[T]:
        pass

    @abstractmethod
    def recuperar_por_id(self, id: TId) -> T:
        pass

    @abstractmethod
    def atualizar(self, dados: T) -> T:
        pass

    @abstractmethod
    def close(self):
        pass
