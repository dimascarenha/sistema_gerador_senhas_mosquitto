import tkinter as tk

from atendente import Atendente


class InterfaceAtendente:


    def __init__(self):

        # Cria o objeto do backend
        self.atendente = Atendente()

        # Conecta no MQTT
        self.atendente.conectar()

        # Assina o tópico de novas senhas
        self.atendente.assinar(
            "senha/nova"
        )


        self.janela = tk.Tk()

        self.janela.title(
            "Atendente"
        )

        self.janela.geometry(
            "600x500"
        )


        titulo = tk.Label(
            self.janela,
            text="ATENDENTE",
            font=("Arial", 30, "bold")
        )

        titulo.pack(
            pady=30
        )


        self.proxima_label = tk.Label(
            self.janela,
            text="Próxima senha: Nenhuma",
            font=("Arial", 25)
        )

        self.proxima_label.pack(
            pady=30
        )


        self.quantidade_label = tk.Label(
            self.janela,
            text="Aguardando: 0",
            font=("Arial", 20)
        )

        self.quantidade_label.pack(
            pady=20
        )


        botao = tk.Button(
            self.janela,
            text="CHAMAR PRÓXIMA",
            font=("Arial", 25, "bold"),
            width=20,
            height=3,
            bg="#1976D2",
            fg="white",
            command=self.chamar
        )

        botao.pack(
            pady=50
        )


        self.janela.protocol(
            "WM_DELETE_WINDOW",
            self.fechar
        )



    def chamar(self):

        self.atendente.chamar_proxima()


        if self.atendente.proxima_senha:

            self.proxima_label.config(
                text=f"Próxima senha: {self.atendente.proxima_senha}"
            )

        else:

            self.proxima_label.config(
                text="Próxima senha: Nenhuma"
            )


        self.quantidade_label.config(
            text=f"Aguardando: {len(self.atendente.fila)}"
        )



    def fechar(self):

        self.atendente.desconectar()

        self.janela.destroy()



if __name__ == "__main__":

    app = InterfaceAtendente()

    app.janela.mainloop()