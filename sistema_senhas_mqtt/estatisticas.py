"""
Programa 4: Estatísticas / Histórico.

Este programa assina dois tópicos:
- senha/nova: para contar quantas senhas foram geradas
- senha/chamada: para contar chamadas, calcular tempo médio e salvar histórico
"""

from datetime import datetime
from pathlib import Path

from cliente_mqtt import ClienteMQTT
from mensagens import Mensagens
import time

class Estatisticas(ClienteMQTT):
    """
    Classe responsável por acompanhar as estatísticas do sistema.

    No diagrama:
    - totalGeradas: quantidade de senhas emitidas
    - totalChamadas: quantidade de senhas chamadas
    - tempoMedio: média do tempo entre gerar e chamar uma senha
    """

    def __init__(self, broker: str = "localhost", porta: int = 1883):
        super().__init__(broker, porta, id_cliente="estatisticas")

        self.total_geradas = 0
        self.total_chamadas = 0
        self.tempo_medio = 0.0

        # Guarda o horário em que cada senha foi gerada.
        # Exemplo: {"A001": datetime(...)}
        self.horarios_geracao = {}

        # Guarda todos os tempos de atendimento em segundos.
        self.tempos_atendimento = []

        # Arquivo onde o histórico será salvo.
        self.arquivo_historico = Path("historico_chamadas.txt")

        # Define o método que será chamado quando chegar uma mensagem MQTT.
        self.ao_receber_mensagem = self.receber_mensagem

    def receber_mensagem(self, topico: str, mensagem: str) -> None:
        """
        Decide o que fazer dependendo do tópico recebido.
        """
        if topico == Mensagens.TOPICO_NOVA_SENHA:
            self.receber_nova_senha(mensagem)
        elif topico == Mensagens.TOPICO_CHAMADA:
            self.receber_chamada(mensagem)

    def receber_nova_senha(self, senha: str) -> None:
        """
        Atualiza as estatísticas quando uma nova senha é criada.
        """
        self.total_geradas += 1
        self.horarios_geracao[senha] = datetime.now()
        self.exibir_estatisticas()

    def receber_chamada(self, senha: str) -> None:
        """
        Atualiza as estatísticas quando uma senha é chamada.
        """
        self.total_chamadas += 1
        self.calcular_tempo_medio(senha)
        self.salvar_historico(senha)
        self.exibir_estatisticas()

    def calcular_tempo_medio(self, senha: str) -> None:
        """
        Calcula o tempo médio entre a geração e a chamada das senhas.
        """
        horario_geracao = self.horarios_geracao.get(senha)

        # Se a Estatísticas foi aberta depois que a senha foi gerada,
        # talvez ela não conheça o horário de criação daquela senha.
        if horario_geracao is None:
            return

        tempo = (datetime.now() - horario_geracao).total_seconds()
        self.tempos_atendimento.append(tempo)
        self.tempo_medio = sum(self.tempos_atendimento) / len(self.tempos_atendimento)

    def salvar_historico(self, senha: str) -> None:
        """
        Salva a senha chamada em um arquivo de texto.
        """
        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        with self.arquivo_historico.open("a", encoding="utf-8") as arquivo:
            arquivo.write(f"{horario} - Senha chamada: {senha}\n")

    def exibir_estatisticas(self) -> None:
        """
        Mostra as estatísticas atuais no terminal.
        """
        aguardando = self.total_geradas - self.total_chamadas
        minutos = int(self.tempo_medio // 60)
        segundos = int(self.tempo_medio % 60)

        print("========== ESTATÍSTICAS ==========")
        print(f"Total de senhas geradas:  {self.total_geradas}")
        print(f"Total de senhas chamadas: {self.total_chamadas}")
        print(f"Aguardando atendimento:   {aguardando}")
        print(f"Tempo médio atendimento:  {minutos:02d}:{segundos:02d}")
        print("==================================")

    def iniciar(self) -> None:
        """
        Inicia o programa de Estatísticas.
        """
        self.conectar()
        self.assinar(Mensagens.TOPICO_NOVA_SENHA)
        self.assinar(Mensagens.TOPICO_CHAMADA)

        print("=== ESTATÍSTICAS / HISTÓRICO ===")
        print("Aguardando mensagens...")
        print(f"Histórico salvo em: {self.arquivo_historico.resolve()}")
        print("Pressione Ctrl+C para sair.")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Programa encerrado pelo usuário.")
        finally:
            self.desconectar()


if __name__ == "__main__":
    estatisticas = Estatisticas()
    estatisticas.iniciar()
