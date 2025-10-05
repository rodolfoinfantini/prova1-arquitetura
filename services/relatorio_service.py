from interfaces.relatorio_service import IRelatorioService
from interfaces.repository import Repository, ReadonlyRepository, Savable
from models.pedido import Pedido
from models.cliente import Cliente
from typing import Generic, TypeVar


T = TypeVar("T")


class SalvarEmArquivo(Generic[T], Savable[T]):
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def salvar(self, dados: T) -> T:
        with open(self.arquivo, 'w') as f:
            f.write(f"{dados}")


class RelatorioVendasService(IRelatorioService):
    def __init__(self, pedido_repository: Repository[Pedido, int], save_service: Savable[str]):
        self.pedido_repository = pedido_repository
        self.save_service = save_service

    def gerar_relatorio(self):
        pedidos = self.pedido_repository.recuperar_tudo()
        print("=== RELATÓRIO DE VENDAS ===")
        total_geral = 0
        for pedido in pedidos:
            print(f"Pedido #{pedido.id} - Cliente: {pedido.cliente.email
                                                    } - Total: R${pedido.total:.2f} - Status: {pedido.status.value}")
            total_geral += pedido.total

        print(f"Total Geral: R${total_geral:.2f}")
        self.save_service.salvar(f"Total de vendas: {total_geral}")


class RelatorioClientesService(IRelatorioService):
    def __init__(self, cliente_repository: ReadonlyRepository[Cliente, str], pedido_repository: Repository[Pedido, int], save_service: Savable[str]):
        self.cliente_repository = cliente_repository
        self.pedido_repository = pedido_repository
        self.save_service = save_service

    def gerar_relatorio(self):
        print("=== RELATÓRIO DE CLIENTES ===")
        clientes = self.cliente_repository.recuperar_tudo()
        save_text = ""
        for cliente in clientes:
            total = self.calcular_total(cliente.email)
            save_text += f"{cliente.email},{cliente.tipo.nome}\n"
            print(f"Cliente: {cliente.email} ({
                  cliente.tipo.nome}) - Total gasto: R${total:.2f}")

        self.save_service.salvar(save_text)

    def calcular_total(self, email):
        pedidos_cliente = self.pedido_repository.rodar_select(
            "SELECT * FROM ped WHERE cli=?", (email,))
        total = 0
        for pedido in pedidos_cliente:
            total += pedido.total
        return total
