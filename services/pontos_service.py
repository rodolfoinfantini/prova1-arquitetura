from interfaces.pontos_service import IPontosService
from interfaces.acao_status import AcaoPosStatus
from models.pedido import Pedido


class PontosService(IPontosService, AcaoPosStatus):
    def ganhar_pontos(self, pedido: Pedido):
        pontos = int(pedido.total * pedido.cliente.tipo.pontos_multi)
        print(f"Cliente {pedido.cliente.tipo.nome} ganhou {pontos} pontos!")

    def executar(self, pedido: Pedido):
        self.ganhar_pontos(pedido)
