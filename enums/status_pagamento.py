from enum import Enum


class StatusPagamento(Enum):
    APROVADO = "aprovado"
    RECUSADO = "recusado"
    PENDENTE = "pendente"
