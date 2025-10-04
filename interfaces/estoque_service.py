from abc import ABC, abstractmethod
from models.item_pedido import ItemPedido


class IEstoqueService(ABC):
    @abstractmethod
    def tem_estoque(self, itens: list[ItemPedido]):
        pass
