from models.pedido import Pedido
from models.cliente import Cliente
from models.item_pedido import ItemPedido
from enums.tipo_pedido import TipoPedido
from enums.status_pedido import StatusPedido
from datetime import datetime


class PedidoEspecial(Pedido):
    TAXA = 1.15
    TIPO = TipoPedido.ESPECIAL

    def __init__(self, cliente: Cliente, itens: list[ItemPedido], status: StatusPedido):
        self.cliente = cliente
        self.itens = itens
        self.status = status
        self.data = datetime.now()
        self.calcular_total()

    def calcular_total(self) -> float:
        total_items = super()._calcular_total_itens()
        self.total = total_items * self.TAXA
        return self.total
