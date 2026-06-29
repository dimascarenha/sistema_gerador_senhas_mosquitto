# Sistema de Senhas com MQTT e Python

Este projeto implementa o sistema do diagrama de classes enviado:

- `ClienteMQTT`: classe base usada por todos os clientes.
- `GeradorSenhas`: publica novas senhas no tópico `senha/nova`.
- `Atendente`: assina `senha/nova` e publica chamadas em `senha/chamada`.
- `Painel`: assina `senha/chamada` e exibe a senha atual.
- `Estatisticas`: assina `senha/nova` e `senha/chamada`, mostra contadores e salva histórico.
- `Mensagens`: centraliza os tópicos MQTT.

Todos os programas são independentes e se comunicam apenas pelo broker Mosquitto.

## 1. Instalar dependências

Abra um terminal dentro desta pasta e execute:

```bash
pip install -r requirements.txt
```

Também é necessário ter o Mosquitto instalado e rodando.

## 2. Iniciar o Mosquitto

Em uma janela de terminal:

```bash
mosquitto -v
```

Se o Mosquitto já estiver instalado como serviço no Windows, talvez ele já esteja rodando.

## 3. Abrir os programas

Abra quatro janelas de terminal dentro desta pasta.

Terminal 1:

```bash
python gerador_senhas.py
```

Terminal 2:

```bash
python atendente.py
```

Terminal 3:

```bash
python painel.py
```

Terminal 4:

```bash
python estatisticas.py
```

## 4. Como apresentar

1. No `Gerador de Senhas`, pressione Enter.
2. Ele cria uma senha, por exemplo `A001`, e publica em `senha/nova`.
3. O `Atendente` recebe automaticamente essa senha.
4. No `Atendente`, pressione Enter para chamar a próxima senha.
5. Ele publica `A001` em `senha/chamada`.
6. O `Painel` recebe e mostra a senha atual.
7. O programa de `Estatisticas` também recebe a chamada, atualiza os contadores e salva no histórico.

## Explicação para o professor

Cada programa é independente e executa como um processo separado. Nenhum deles conhece diretamente os demais. Todos se comunicam exclusivamente por meio do broker Mosquitto utilizando o protocolo MQTT.

Quando o `Atendente` publica uma senha chamada em `senha/chamada`, a mesma mensagem pode ser recebida pelo `Painel` e pelo programa de `Estatisticas`. Isso demonstra o modelo Publish/Subscribe.
