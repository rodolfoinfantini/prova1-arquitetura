from abc import ABC, abstractmethod
from models.pedido import Pedido
from enums.status_pagamento import StatusPagamento


class IPagamentoService(ABC):
    @abstractmethod
    def processar_pagamento(self, pedido: Pedido, valor: float) -> StatusPagamento:
        pass
