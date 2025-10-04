from models.item_pedido import ItemPedido
from models.cliente import Cliente
from enums.tipo_item import TipoItem
from enums.tipo_cliente import TipoCliente
from enums.metodo_pagamento import MetodoPagamento
from services.pedido_service import PedidoService
from services.estoque_service import EstoqueService
from repositories.pedido_repository import PedidoRepository
from repositories.produto_repository import ProdutoRepositorySimplificado


def main():
    pedido_repository = PedidoRepository()
    produtos_repository = ProdutoRepositorySimplificado()
    estoque_service = EstoqueService(produtos_repository)
    pedido_service = PedidoService(pedido_repository, estoque_service)

    items = [
        ItemPedido('produto1', 100, 1, TipoItem.NORMAL),
        ItemPedido('produto2', 50, 2, TipoItem.DESC10)
    ]
    cliente = Cliente('cliente@exemplo.com', TipoCliente.NORMAL)

    pedido = pedido_service.criar_pedido(cliente, items)

    pedido_service.processar_pagamento(pedido.id, MetodoPagamento.PIX, 200)

    print(pedido)


if __name__ == '__main__':
    main()
