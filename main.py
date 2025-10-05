from database.conexao import SqliteConexao
from models.item_pedido import ItemPedido
from models.cliente import Cliente
from enums.tipo_item import TipoItem
from enums.tipo_cliente import TipoCliente
from enums.metodo_pagamento import MetodoPagamento
from services.pedido_service import PedidoService, PedidoEspecialService
from services.estoque_service import EstoqueService
from services.relatorio_service import RelatorioClientesService, RelatorioVendasService, SalvarEmArquivo
from repositories.pedido_repository import PedidoRepository
from repositories.produto_repository import ProdutoRepositorySimplificado
from repositories.cliente_repository import ClienteRepository
from services.notificacao_service import SmsNotificacaoService, EmailNotificacaoService
from services.pontos_service import PontosService


def main():
    conexao = SqliteConexao('loja.db')

    acoes_pos_status = [SmsNotificacaoService(
    ), EmailNotificacaoService(), PontosService()]
    acoes_pos_criacao = [EmailNotificacaoService()]
    pedido_repository = PedidoRepository(conexao)
    pedido_service = PedidoService(
        pedido_repository, EstoqueService(ProdutoRepositorySimplificado()), acoes_pos_status, acoes_pos_criacao)

    items = [
        ItemPedido('produto1', 100, 1, TipoItem.NORMAL),
        ItemPedido('produto2', 50, 2, TipoItem.DESC10)
    ]
    cliente = Cliente('cliente@exemplo.com', TipoCliente.NORMAL)

    pedido = pedido_service.criar_pedido(cliente, items)

    pedido_service.processar_pagamento(pedido.id, MetodoPagamento.PIX, 200)

    relatorio_vendas_service = RelatorioVendasService(
        pedido_repository, SalvarEmArquivo('rel_vendas.txt'))
    relatorio_clientes_service = RelatorioClientesService(
        ClienteRepository(conexao), pedido_repository, SalvarEmArquivo('rel_clientes.txt'))

    relatorio_vendas_service.gerar_relatorio()
    relatorio_clientes_service.gerar_relatorio()


if __name__ == '__main__':
    main()
