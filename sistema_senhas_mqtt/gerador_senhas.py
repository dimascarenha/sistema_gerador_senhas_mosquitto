"""
Programa 1: Gerador de Senhas.

Este programa representa o cliente do banco/posto de saúde.
Quando o usuário pressiona Enter, uma nova senha é criada e publicada
no tópico MQTT "senha/nova".
"""

from cliente_mqtt import ClienteMQTT
from mensagens import Mensagens


class GeradorSenhas(ClienteMQTT):
    """
    Classe responsável por gerar senhas no formato A001, A002, A003...

    No diagrama de classes, ela herda de ClienteMQTT.
    Isso significa que ela reutiliza os métodos conectar(), publicar() e
    desconectar().
    """

    def __init__(self, broker: str = "localhost", porta: int = 1883):
        super().__init__(broker, porta, id_cliente="gerador-senhas")

        # Contador usado para montar a próxima senha.
        self.contador = 0

        # Formato da senha. O número será preenchido com 3 dígitos.
        self.formato = "A{:03d}"

    def gerar_senha(self) -> str:
        """
        Gera uma nova senha seguindo o formato A001, A002, A003...
        """
        self.contador += 1
        return self.formato.format(self.contador)

    def enviar_senha(self) -> None:
        """
        Gera uma senha e publica no tópico senha/nova.
        """
        senha = self.gerar_senha()
        self.publicar(Mensagens.TOPICO_NOVA_SENHA, senha)
        print(f"Nova senha gerada: {senha}")

    def iniciar(self) -> None:
        """
        Inicia o programa do Gerador.

        O loop fica aguardando Enter para gerar senha.
        Digitar S permite sair do programa.
        """
        self.conectar()

        print("=== GERADOR DE SENHAS ===")
        print("Pressione Enter para gerar uma nova senha.")
        print("Digite S e pressione Enter para sair.")

        try:
            while True:
                comando = input("Gerar senha? ")

                if comando.strip().lower() == "s":
                    break

                self.enviar_senha()
        except KeyboardInterrupt:
            print("Programa encerrado pelo usuário.")
        finally:
            self.desconectar()


if __name__ == "__main__":
    gerador = GeradorSenhas()
    gerador.iniciar()
