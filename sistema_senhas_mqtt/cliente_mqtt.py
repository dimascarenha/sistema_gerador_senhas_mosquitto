"""
Classe base ClienteMQTT.

Todos os programas do sistema são clientes MQTT:
- Gerador de Senhas
- Atendente
- Painel
- Estatisticas

Como todos precisam conectar, desconectar, publicar e assinar tópicos,
esses comportamentos comuns ficam centralizados nesta classe.
"""

from __future__ import annotations

import uuid
from typing import Callable, Optional

import paho.mqtt.client as mqtt


class ClienteMQTT:
    """
    Classe base para todos os clientes MQTT do projeto.

    A classe representa a parte comum do diagrama:
    - cliente: objeto mqtt.Client
    - broker: endereço do Mosquitto
    - porta: porta usada pelo MQTT
    - id_cliente: identificador único do cliente
    """

    def __init__(
        self,
        broker: str = "localhost",
        porta: int = 1883,
        id_cliente: Optional[str] = None,
    ):
        # Endereço do broker MQTT.
        self.broker = broker

        # Porta padrão do MQTT.
        self.porta = porta

        # Identificador único do cliente.
        self.id_cliente = id_cliente or f"cliente-{uuid.uuid4()}"

        # Cria o cliente MQTT (compatível com versões antigas e novas).
        try:
            self.cliente = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                client_id=self.id_cliente,
            )
        except (AttributeError, TypeError):
            self.cliente = mqtt.Client(client_id=self.id_cliente)

        # Callback definido pelas classes filhas.
        self.ao_receber_mensagem: Optional[Callable[[str, str], None]] = None

        # Associa os eventos do MQTT aos métodos desta classe.
        self.cliente.on_connect = self._quando_conectar
        self.cliente.on_message = self._quando_receber_mensagem

    def conectar(self) -> None:
        """
        Conecta ao broker e inicia o loop MQTT.
        """
        print(f"Conectando ao broker Mosquitto em {self.broker}:{self.porta}...")
        self.cliente.connect(self.broker, self.porta)
        self.cliente.loop_start()

    def desconectar(self) -> None:
        """
        Encerra o loop MQTT e desconecta do broker.
        """
        print("Desconectando do Mosquitto...")
        self.cliente.loop_stop()
        self.cliente.disconnect()

    def publicar(self, topico: str, mensagem: str) -> None:
        """
        Publica uma mensagem em um tópico MQTT.
        """
        resultado = self.cliente.publish(topico, mensagem)

        if resultado.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Publicado no tópico '{topico}': {mensagem}")
        else:
            print("Erro ao publicar mensagem.")

    def assinar(self, topico: str) -> None:
        """
        Assina um tópico MQTT.
        """
        self.cliente.subscribe(topico)
        print(f"Assinando o tópico '{topico}'")

    def definir_callback(self, callback: Callable[[str, str], None]) -> None:
        """
        Define a função chamada quando uma mensagem for recebida.
        """
        self.ao_receber_mensagem = callback

    def _quando_conectar(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties=None,
    ) -> None:
        """
        Executado automaticamente quando a conexão com o broker é estabelecida.
        """
        if reason_code.is_failure:
            print(f"Falha ao conectar ao Mosquitto: {reason_code}")
        else:
            print("Conectado ao Mosquitto com sucesso.")

    def _quando_receber_mensagem(self, client, userdata, msg) -> None:
        """
        Executado automaticamente quando uma mensagem MQTT é recebida.
        """
        topico = msg.topic
        mensagem = msg.payload.decode("utf-8")

        if self.ao_receber_mensagem is not None:
            self.ao_receber_mensagem(topico, mensagem)