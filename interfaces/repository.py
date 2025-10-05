from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
TId = TypeVar("TId")


class ReadonlyRepository(ABC, Generic[T, TId]):
    @abstractmethod
    def recuperar_tudo(self) -> list[T]:
        pass

    @abstractmethod
    def recuperar_por_id(self, id: TId) -> T:
        pass

    @abstractmethod
    def rodar_select(self, select: str, params=None) -> list[T]:
        pass


class Savable(ABC, Generic[T]):
    @abstractmethod
    def salvar(self, dados: T) -> T:
        pass


class Repository(Generic[T, TId], ReadonlyRepository[T, TId], Savable[T]):
    @abstractmethod
    def atualizar(self, dados: T) -> T:
        pass

    @abstractmethod
    def close(self):
        pass
