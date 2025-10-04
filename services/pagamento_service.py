from abc import abstractmethod
from interfaces.pagamento_service import IPagamentoService
from models.pedido import Pedido
from enums.status_pagamento import StatusPagamento


class PagamentoServiceBase(IPagamentoService):
    def processar_pagamento(self, pedido: Pedido, valor: float) -> StatusPagamento:
        if (valor < pedido.total):
            print('Valor insuficiente!')
            return StatusPagamento.RECUSADO

        return self._processar_pagamento(valor)

    @abstractmethod
    def _processar_pagamento(self, valor: float) -> StatusPagamento:
        pass


class CartaoPagamentoService(PagamentoServiceBase):
    def _processar_pagamento(self, valor: float) -> StatusPagamento:
        print("Processando pagamento com cartao...")
        print("Cartao validado!")
        return StatusPagamento.APROVADO


class PixPagamentoService(PagamentoServiceBase):
    def _processar_pagamento(self, valor: float) -> StatusPagamento:
        print("Gerando QR Code PIX...")
        print("PIX recebido!")
        return StatusPagamento.APROVADO


class BoletoPagamentoService(PagamentoServiceBase):
    def _processar_pagamento(self, valor: float) -> StatusPagamento:
        print("Gerando boleto ...")
        print("Boleto gerado!")
        return StatusPagamento.PENDENTE
