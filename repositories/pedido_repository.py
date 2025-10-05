from interfaces.repository import Repository
from models.pedido import Pedido
from models.item_pedido import ItemPedido
from models.cliente import Cliente
from enums.tipo_item import TipoItem
from enums.tipo_cliente import TipoCliente
from enums.status_pedido import StatusPedido
from datetime import datetime
from interfaces.conexao import IConexao
import json


class PedidoRepository(Repository[Pedido, int]):
    DATE_PATTERN = '%Y-%m-%d %H:%M:%S'

    def __init__(self, conexao: IConexao):
        (self.db, self.cursor) = conexao.get_conexao()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ped (
            id INTEGER PRIMARY KEY,
            cli TEXT,
            itens TEXT,
            tot REAL,
            st TEXT,
            dt TEXT,
            tp TEXT)''')
        self.db.commit()

    def salvar(self, dados: Pedido) -> Pedido:
        itens_json = self.__gerar_json_itens(dados.itens)
        self.cursor.execute(
            "INSERT INTO ped (cli, itens, tot, st, dt, tp) VALUES (?, ?, ?, ?, ?, ?)",
            (dados.cliente.email, itens_json, dados.total, dados.status.value,
             dados.data.strftime(self.DATE_PATTERN), dados.cliente.tipo.nome)
        )
        self.db.commit()
        dados.id = self.cursor.lastrowid
        return dados

    def recuperar_por_id(self, id: int) -> Pedido:
        pedidos = self.rodar_select("SELECT * FROM ped WHERE id=?", (id,))
        if len(pedidos) == 0:
            raise Exception(f"Pedido não encontrado com Id: {id}")

        return pedidos[0]

    def recuperar_tudo(self) -> list[Pedido]:
        pedidos = self.rodar_select("SELECT * FROM ped")
        return pedidos

    def atualizar(self, dados: Pedido) -> Pedido:
        itens_json = self.__gerar_json_itens(dados.itens)
        self.cursor.execute(
            "UPDATE ped SET cli=?, itens=?, tot=?, st=?, dt=?, tp=? WHERE id=?",
            (dados.cliente.email, itens_json, dados.total, dados.status.value,
             dados.data.strftime(self.DATE_PATTERN), dados.cliente.tipo.nome,
             dados.id)
        )
        self.db.commit()

        return self.recuperar_por_id(dados.id)

    def rodar_select(self, select: str, params=None) -> list[Pedido]:
        if params:
            self.cursor.execute(select, params)
        else:
            self.cursor.execute(select)

        pedidos = self.cursor.fetchall()
        return [self.__converter_banco_para_modelo_pedido(row) for row in pedidos]

    def close(self):
        self.db.close()

    def __converter_banco_para_modelo_pedido(self, row: list) -> Pedido:
        pedido = Pedido()
        pedido.id = row[0]
        pedido.cliente = Cliente(row[1], TipoCliente.from_nome(row[6]))
        pedido.itens = self.__converter_banco_para_modelo_itens(row[2])
        pedido.total = row[3]
        pedido.data = datetime.strptime(row[5], self.DATE_PATTERN)
        pedido.status = StatusPedido(row[4])

        return pedido

    def __converter_banco_para_modelo_itens(self, itens_json: str) -> list[ItemPedido]:
        itens_banco = json.loads(itens_json)
        return [ItemPedido(item_banco['nome'], item_banco['p'], item_banco['q'], TipoItem.from_nome(item_banco['tipo'])) for item_banco in itens_banco]

    def __gerar_json_itens(self, itens: list[ItemPedido]) -> str:
        return json.dumps(self.__converter_itens_para_o_banco(itens))

    def __converter_itens_para_o_banco(self, itens: list[ItemPedido]) -> list:
        return [
            {
                'nome': item.nome,
                'p': item.preco,
                'q': item.quantidade,
                'tipo': item.tipo.nome
            } for item in itens]
