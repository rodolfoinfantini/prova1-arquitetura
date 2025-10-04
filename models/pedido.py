from dataclasses import dataclass
from models.cliente import Cliente
from models.item_pedido import ItemPedido
from enums.status_pedido import StatusPedido
from enums.tipo_pedido import TipoPedido
from datetime import datetime


@dataclass
class Pedido:
    TIPO = TipoPedido.NORMAL

    id: int
    cliente: Cliente
    itens: list[ItemPedido]
    total: float
    status: StatusPedido
    data: datetime

    def __init__(self, cliente: Cliente = None, itens: list[ItemPedido] = None, status: StatusPedido = None):
        if cliente and itens and status:
            self.cliente = cliente
            self.itens = itens
            self.status = status
            self.data = datetime.now()
            self.calcular_total()

    def __calcular_total_itens(self) -> float:
        total = 0
        for item in self.itens:
            total += item.calcular_total()
        return total

    def calcular_total(self) -> float:
        total_items = self.__calcular_total_itens()
        self.total = self.cliente.tipo.estrategia_desconto.aplicar_desconto(
            total_items)
        return self.total
