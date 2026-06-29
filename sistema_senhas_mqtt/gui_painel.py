import tkinter as tk

from painel import Painel
from mensagens import Mensagens


class InterfacePainel:


    def __init__(self):

        # Backend do painel MQTT
        self.painel = Painel()


        # Quando chegar uma mensagem MQTT,
        # chama a função da interface
        self.painel.ao_receber_mensagem = self.receber_senha


        # Conecta ao Mosquitto
        self.painel.conectar()


        # Assina o tópico de chamadas
        self.painel.assinar(
            Mensagens.TOPICO_CHAMADA
        )


        # Criando janela
        self.janela = tk.Tk()

        self.janela.title(
            "Painel de Chamadas"
        )


        # Tela cheia
        self.janela.attributes(
            "-fullscreen",
            True
        )


        # Título
        titulo = tk.Label(
            self.janela,
            text="SENHA ATUAL",
            font=("Arial", 50, "bold")
        )

        titulo.pack(
            pady=50
        )


        # Senha exibida
        self.senha_label = tk.Label(
            self.janela,
            text="---",
            font=("Arial", 120, "bold"),
            fg="blue"
        )

        self.senha_label.pack(
            expand=True
        )


        # Mensagem inferior
        mensagem = tk.Label(
            self.janela,
            text="Por favor, dirija-se ao atendimento.",
            font=("Arial", 30)
        )

        mensagem.pack(
            pady=50
        )


        # ESC sai do modo tela cheia
        self.janela.bind(
            "<Escape>",
            self.sair_tela_cheia
        )


        self.janela.protocol(
            "WM_DELETE_WINDOW",
            self.fechar
        )



    def receber_senha(
        self,
        topico,
        mensagem
    ):

        if topico == Mensagens.TOPICO_CHAMADA:


            # Guarda a senha recebida
            self.painel.senha_atual = mensagem


            # Atualiza a tela
            self.senha_label.config(
                text=mensagem
            )



    def sair_tela_cheia(
        self,
        evento=None
    ):

        self.janela.attributes(
            "-fullscreen",
            False
        )



    def fechar(self):

        self.painel.desconectar()

        self.janela.destroy()



if __name__ == "__main__":

    app = InterfacePainel()

    app.janela.mainloop()