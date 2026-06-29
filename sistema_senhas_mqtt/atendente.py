"""
Programa 2: Atendente.

Este programa assina o tópico "senha/nova" para receber as senhas geradas.
Quando o atendente pressiona Enter, a próxima senha da fila é chamada e
publicada no tópico "senha/chamada".
"""

from collections import deque

from cliente_mqtt import ClienteMQTT
from mensagens import Mensagens


class Atendente(ClienteMQTT):
    """
    Classe responsável por receber novas senhas e chamar a próxima.

    No diagrama:
    - proximaSenha: senha que está no início da fila
    - fila: estrutura que guarda as senhas aguardando atendimento
    """

    def __init__(self, broker: str = "localhost", porta: int = 1883):
        super().__init__(broker, porta, id_cliente="atendente")

        # deque é uma fila eficiente: a primeira senha que entra é a primeira que sai.
        self.fila = deque()

        # Guarda a próxima senha exibida ao atendente.
        self.proxima_senha = None

        # Define qual método será executado quando uma mensagem MQTT chegar.
        self.ao_receber_mensagem = self.receber_senha

    def receber_senha(self, topico: str, mensagem: str) -> None:
        """
        Recebe uma senha publicada pelo Gerador no tópico senha/nova.
        """
        if topico == Mensagens.TOPICO_NOVA_SENHA:
            self.fila.append(mensagem)
            self.proxima_senha = self.fila[0]

            print("Senha recebida:")
            print(mensagem)
            self.exibir_proxima()

    def exibir_proxima(self) -> None:
        """
        Mostra a próxima senha que será chamada.
        """
        if self.fila:
            print(f"Próxima senha na fila: {self.fila[0]}")
            print(f"Total aguardando: {len(self.fila)}")
        else:
            print("Nenhuma senha aguardando atendimento.")

    def chamar_proxima(self) -> None:
        """
        Remove a próxima senha da fila e publica no tópico senha/chamada.
        """
        if not self.fila:
            print("Não há senhas para chamar.")
            return

        senha = self.fila.popleft()
        self.proxima_senha = self.fila[0] if self.fila else None
        self.publicar_chamada(senha)
        self.exibir_proxima()

    def publicar_chamada(self, senha: str) -> None:
        """
        Publica a senha chamada para que Painel e Estatísticas recebam.
        """
        self.publicar(Mensagens.TOPICO_CHAMADA, senha)
        print(f"Senha chamada: {senha}")

    def iniciar(self) -> None:
        """
        Inicia o programa do Atendente.

        Primeiro conecta ao Mosquitto, depois assina o tópico senha/nova.
        O loop fica aguardando Enter para chamar a próxima senha.
        """
        self.conectar()
        self.assinar(Mensagens.TOPICO_NOVA_SENHA)

        print("=== ATENDENTE ===")
        print("Aguardando senhas novas...")
        print("Pressione Enter para chamar a próxima senha.")
        print("Digite S e pressione Enter para sair.")

        try:
            while True:
                comando = input("Chamar próxima? ")

                if comando.strip().lower() == "s":
                    break

                self.chamar_proxima()
        except KeyboardInterrupt:
            print("Programa encerrado pelo usuário.")
        finally:
            self.desconectar()


if __name__ == "__main__":
    atendente = Atendente()
    atendente.iniciar()
