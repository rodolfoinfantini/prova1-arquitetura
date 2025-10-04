from dataclasses import dataclass
from enums.tipo_cliente import TipoCliente


@dataclass
class Cliente:
    def __init__(self, email: str, tipo: TipoCliente):
        self.email = email
        self.tipo = tipo

    email: str
    tipo: TipoCliente
