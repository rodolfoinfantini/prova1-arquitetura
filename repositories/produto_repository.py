from interfaces.repository import Repository
from models.produto import Produto


class ProdutoRepositorySimplificado(Repository[Produto, str]):
    def __init__(self):
        self.database = [
            Produto('produto1', 100),
            Produto('produto2', 50),
            Produto('produto3', 75),
        ]

    def salvar(self, dados: Produto) -> Produto:
        self.database.append(dados)
        return dados

    def recuperar_tudo(self) -> list[Produto]:
        return [Produto(produto.name, produto.estoque) for produto in self.database]

    def recuperar_por_id(self, id: str) -> Produto:
        for produto in self.database:
            if produto.nome == id:
                return Produto(produto.nome, produto.estoque)

        raise Exception(f'Produto não encontrado com Id: {id}')

    def atualizar(self, dados: Produto) -> Produto:
        for produto in self.database:
            if produto.nome == dados.nome:
                produto.estoque = dados.estoque
        return Produto(produto.nome, produto.estoque)

    def rodar_select(self, select: str, params=None) -> list[Produto]:
        return self.recuperar_tudo()

    def close(self):
        self.database = []
