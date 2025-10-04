from interfaces.estoque_service import IEstoqueService
from interfaces.repository import Repository
from models.produto import Produto
from models.item_pedido import ItemPedido


class EstoqueService(IEstoqueService):
    def __init__(self, produtos_repository: Repository[Produto, str]):
        self.produtos_repository = produtos_repository

    def tem_estoque(self, itens: list[ItemPedido]):
        for item in itens:
            item_salvo = self.produtos_repository.recuperar_por_id(item.nome)
            if item_salvo.estoque < item.quantidade:
                print(f"Estoque insuficiente para {item.nome}")
                return False
        return True
