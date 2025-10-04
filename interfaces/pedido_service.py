from abc import ABC, abstractmethod
from models.cliente import Cliente
from models.item_pedido import ItemPedido
from models.pedido import Pedido
from enums.status_pedido import StatusPedido
from enums.metodo_pagamento import MetodoPagamento


class IPedidoService(ABC):
    @abstractmethod
    def criar_pedido(self, cliente: Cliente, itens: list[ItemPedido]) -> Pedido:
        pass

    @abstractmethod
    def atualizar_status(self, id: int, status: StatusPedido) -> Pedido:
        pass

    @abstractmethod
    def processar_pagamento(self, id: int, metodo_pagamento: MetodoPagamento, valor: float) -> bool:
        pass
