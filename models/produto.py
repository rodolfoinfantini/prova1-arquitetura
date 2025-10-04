from dataclasses import dataclass


@dataclass
class Produto:
    def __init__(self, nome: str, estoque: float):
        self.nome = nome
        self.estoque = estoque

    nome: str
    estoque: float
