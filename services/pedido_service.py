from interfaces.pedido_service import IPedidoService
from interfaces.estoque_service import IEstoqueService
from interfaces.repository import Repository
from interfaces.acao_status import AcaoPosStatus
from enums.status_pedido import StatusPedido
from enums.metodo_pagamento import MetodoPagamento
from enums.status_pagamento import StatusPagamento
from models.pedido import Pedido
from models.cliente import Cliente
from models.item_pedido import ItemPedido


class PedidoService(IPedidoService):
    def __init__(self, pedido_repository: Repository[Pedido, int], estoque_service: IEstoqueService, acoes_pos_status: list[AcaoPosStatus], acoes_pos_criacao: list[AcaoPosStatus]):
        self.pedido_repository = pedido_repository
        self.estoque_service = estoque_service
        self.acoes_pos_status = acoes_pos_status
        self.acoes_pos_criacao = acoes_pos_criacao

    def criar_pedido(self, cliente: Cliente, itens: list[ItemPedido]) -> Pedido:
        pedido = Pedido(cliente, itens, StatusPedido.PENDENTE)

        if not self.estoque_service.tem_estoque(itens):
            raise Exception("Estoque indisponível")

        pedido_salvo = self.pedido_repository.salvar(pedido)

        self._executar_acoes(self.acoes_pos_criacao, pedido_salvo)

        return pedido_salvo

    def atualizar_status(self, id: int, status: StatusPedido) -> Pedido:
        pedido = self.pedido_repository.recuperar_por_id(id)
        pedido.status = status
        pedido_salvo = self.pedido_repository.atualizar(pedido)

        self._executar_acoes(self.acoes_pos_status, pedido)

        return pedido_salvo

    def processar_pagamento(self, id: int, metodo_pagamento: MetodoPagamento, valor: float) -> bool:
        pedido = self.pedido_repository.recuperar_por_id(id)
        status = metodo_pagamento.service.processar_pagamento(pedido, valor)
        if status == StatusPagamento.APROVADO:
            self.atualizar_status(pedido.id, StatusPedido.APROVADO)
        elif status == StatusPagamento.RECUSADO:
            return False

        return True

    def _executar_acoes(self, acoes: list[AcaoPosStatus], pedido: Pedido):
        for acao in acoes:
            acao.executar(pedido)
