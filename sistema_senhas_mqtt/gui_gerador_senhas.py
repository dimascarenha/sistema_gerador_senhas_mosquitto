import tkinter as tk

from gerador_senhas import GeradorSenhas


class InterfaceGerador:


    def __init__(self):

        self.gerador = GeradorSenhas()

        # Conecta ao MQTT
        self.gerador.conectar()


        # Janela
        self.janela = tk.Tk()

        self.janela.title(
            "Gerador de Senhas"
        )

        self.janela.geometry(
            "800x600"
        )


        # Título
        titulo = tk.Label(
            self.janela,
            text="GERADOR DE SENHAS",
            font=("Arial", 40, "bold")
        )

        titulo.pack(
            pady=50
        )


        # Texto explicativo
        descricao = tk.Label(
            self.janela,
            text="Pressione o botão para retirar uma senha",
            font=("Arial", 20)
        )

        descricao.pack(
            pady=20
        )


        # Senha atual
        self.senha_label = tk.Label(
            self.janela,
            text="---",
            font=("Arial", 80, "bold"),
            fg="black"
        )

        self.senha_label.pack(
            expand=True
        )


        # Botão gerar
        botao = tk.Button(
            self.janela,
            text="GERAR SENHA",
            font=("Arial", 30, "bold"),
            width=20,
            height=3,
            bg="#404850",
            fg="white",
            activebackground="#307531",
            activeforeground="white",
            command=self.gerar
        )

        botao.pack(
            pady=50
        )


        self.janela.protocol(
            "WM_DELETE_WINDOW",
            self.fechar
        )



    def gerar(self):

        senha = self.gerador.gerar_senha()


        self.gerador.publicar(
            "senha/nova",
            senha
        )


        self.senha_label.config(
            text=senha
        )



    def fechar(self):

        self.gerador.desconectar()

        self.janela.destroy()



if __name__ == "__main__":

    app = InterfaceGerador()

    app.janela.mainloop()