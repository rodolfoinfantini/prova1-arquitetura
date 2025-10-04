from enum import Enum
from strategies.estrategia_desconto import EstrategiaDesconto, DescontoNormal, Desconto10, Desconto20


class TipoItem(Enum):
    NORMAL = "normal", DescontoNormal()
    DESC10 = "desc10", Desconto10()
    DESC20 = "desc20", Desconto20()

    def __init__(self, nome: str, estrategia_desconto: EstrategiaDesconto):
        self.nome = nome
        self.estrategia_desconto = estrategia_desconto

    @classmethod
    def from_nome(cls, nome: str):
        for m in cls:
            if m.nome == nome:
                return m
        raise ValueError(f"{nome!r} não é um TipoItem válido")
