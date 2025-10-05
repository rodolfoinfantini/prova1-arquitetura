from interfaces.repository import ReadonlyRepository
from interfaces.conexao import IConexao
from models.cliente import Cliente
from enums.tipo_cliente import TipoCliente


class ClienteRepository(ReadonlyRepository[Cliente, str]):
    def __init__(self, conexao: IConexao):
        (self.db, self.cursor) = conexao.get_conexao()

    def recuperar_tudo(self) -> list[Cliente]:
        return self.rodar_select("SELECT DISTINCT cli, tp FROM ped")

    def recuperar_por_id(self, id: str) -> Cliente:
        clientes = self.rodar_select(
            "SELECT DISTINCT cli, tp FROM ped WHERE cli=?", (id))
        if len(clientes) == 0:
            raise Exception(f"Cliente não encontrado com email: {id}")

        return clientes[0]

    def rodar_select(self, select: str, params=None) -> list[Cliente]:
        if params:
            self.cursor.execute(select, params)
        else:
            self.cursor.execute(select)

        clientes = self.cursor.fetchall()
        return [self.__converter_banco_para_modelo(row) for row in clientes]

    def __converter_banco_para_modelo(self, row: list) -> Cliente:
        return Cliente(row[0], TipoCliente.from_nome(row[1]))
