"""
Programa 3: Painel de Chamada.

Este programa apenas escuta o tópico "senha/chamada".
Quando uma senha é chamada pelo Atendente, o Painel mostra a senha atual.
"""

from cliente_mqtt import ClienteMQTT
from mensagens import Mensagens


class Painel(ClienteMQTT):
    """
    Classe responsável por exibir a senha chamada.

    No diagrama:
    - senhaAtual: última senha recebida no tópico senha/chamada
    """

    def __init__(self, broker: str = "localhost", porta: int = 1883):
        super().__init__(broker, porta, id_cliente="painel")

        # Guarda a senha chamada mais recentemente.
        self.senha_atual = None

        # Define o método que processa mensagens recebidas.
        self.ao_receber_mensagem = self.receber_chamada

    def receber_chamada(self, topico: str, mensagem: str) -> None:
        """
        Recebe a senha chamada pelo Atendente.
        """
        if topico == Mensagens.TOPICO_CHAMADA:
            self.senha_atual = mensagem
            self.exibir_senha()

    def exibir_senha(self) -> None:
        """
        Exibe a senha atual em destaque no terminal.
        """
        print(" ==============================")
                   
        print("        SENHA ATUAL")
        print(f"          {self.senha_atual}")
        print("==============================")
        print("Por favor, dirija-se ao atendimento.")

    def iniciar(self) -> None:
        """
        Inicia o programa do Painel.

        Ele apenas fica conectado e aguardando chamadas.
        """
        self.conectar()
        self.assinar(Mensagens.TOPICO_CHAMADA)

        print("=== PAINEL DE CHAMADA ===")
        print("Aguardando senhas chamadas...")
        print("Pressione Ctrl+C para sair.")

        try:
            while True:
                # input() mantém o programa aberto sem consumir processamento.
                input()
        except KeyboardInterrupt:
            print("Programa encerrado pelo usuário.")
        finally:
            self.desconectar()


if __name__ == "__main__":
    painel = Painel()
    painel.iniciar()
