from dataclasses import dataclass
from enums.tipo_item import TipoItem


@dataclass
class ItemPedido:
    def __init__(self, nome: str, preco: float, quantidade: int, tipo: TipoItem):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.tipo = tipo

    nome: str
    preco: float
    quantidade: int
    tipo: TipoItem

    def calcular_total(self) -> float:
        return self.tipo.estrategia_desconto.aplicar_desconto(self.preco * self.quantidade)
