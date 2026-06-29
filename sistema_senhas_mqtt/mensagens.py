"""
Arquivo responsável por centralizar os tópicos MQTT usados no sistema.

No diagrama de classes, esta parte aparece como a classe "Mensagens".
A ideia é evitar escrever o nome dos tópicos várias vezes no código.
Assim, se um tópico precisar mudar, alteramos em apenas um lugar.
"""


class Mensagens:
    # Tópico usado pelo Gerador de Senhas para publicar uma nova senha.
    TOPICO_NOVA_SENHA = "senha/nova"

    # Tópico usado pelo Atendente para publicar a senha chamada.
    TOPICO_CHAMADA = "senha/chamada"
