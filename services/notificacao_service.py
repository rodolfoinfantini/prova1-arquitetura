from interfaces.notificacao_service import INotificacaoService
from interfaces.acao_status import AcaoPosStatus
from models.pedido import Pedido


class EmailNotificacaoService(INotificacaoService, AcaoPosStatus):
    def enviar(self, destino: str, mensagem: str):
        print(f"Email enviado para {destino}: {mensagem}")

    def executar(self, pedido: Pedido):
        self.enviar(pedido.cliente.email, f"Pedido {pedido.status.value}!")


class SmsNotificacaoService(INotificacaoService, AcaoPosStatus):
    def enviar(self, destino: str, mensagem: str):
        print(f"SMS enviado para {destino}: {mensagem}")

    def executar(self, pedido: Pedido):
        self.enviar(pedido.cliente.email, f"Pedido {pedido.status.value}!")
