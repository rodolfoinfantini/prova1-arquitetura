from enum import Enum
from interfaces.pagamento_service import IPagamentoService
from services.pagamento_service import PixPagamentoService, BoletoPagamentoService, CartaoPagamentoService


class MetodoPagamento(Enum):
    CARTAO = "cartao", CartaoPagamentoService()
    PIX = "pix", PixPagamentoService()
    BOLETO = "boleto", BoletoPagamentoService()

    def __init__(self, nome: str, service: IPagamentoService):
        self.nome = nome
        self.service = service
