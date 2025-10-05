from enum import Enum
from strategies.estrategia_desconto import EstrategiaDesconto, DescontoNormal, Desconto5


class TipoCliente(Enum):
    NORMAL = "normal", DescontoNormal(), 1
    VIP = "VIP", Desconto5(), 2  # vip ganha 2x pontos

    def __init__(self, nome: str, estrategia_desconto: EstrategiaDesconto, pontos_multi: float):
        self.nome = nome
        self.estrategia_desconto = estrategia_desconto
        self.pontos_multi = pontos_multi

    @classmethod
    def from_nome(cls, nome: str):
        for m in cls:
            if m.nome == nome:
                return m
        raise ValueError(f"{nome!r} não é um TipoCliente válido")
