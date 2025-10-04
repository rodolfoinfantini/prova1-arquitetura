from enum import Enum
from strategies.estrategia_desconto import EstrategiaDesconto, DescontoNormal, Desconto5


class TipoCliente(Enum):
    NORMAL = "normal", DescontoNormal()
    VIP = "vip", Desconto5()

    def __init__(self, nome: str, estrategia_desconto: EstrategiaDesconto):
        self.nome = nome
        self.estrategia_desconto = estrategia_desconto

    @classmethod
    def from_nome(cls, nome: str):
        for m in cls:
            if m.nome == nome:
                return m
        raise ValueError(f"{nome!r} não é um TipoCliente válido")
