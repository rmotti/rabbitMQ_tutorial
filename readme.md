# 🐰 RabbitMQ Tutorial - Python Implementation

Este repositório contém a implementação prática dos padrões de mensageria utilizando **RabbitMQ** e **Python**. O projeto abrange desde o envio simples de mensagens até padrões complexos de RPC (Remote Procedure Call), simulando cenários reais de Engenharia de Dados e Sistemas Distribuídos.

## 🛠️ Tecnologias Utilizadas
* **RabbitMQ:** Message Broker (rodando em Docker).
* **Python 3:** Linguagem de script.
* **Pika:** Biblioteca cliente Python para AMQP 0-9-1.
* **Docker:** Para orquestração do servidor RabbitMQ.

## 🚀 Configuração do Ambiente

### 1. Subindo o Servidor RabbitMQ
Utilizamos a imagem oficial com o plugin de gerenciamento habilitado:
```bash
docker run -d --name rabbitmq-learning -p 5672:5672 -p 15672:15672 rabbitmq:3-management
Painel de Controle: http://localhost:15672 (User/Pass: guest)

2. Instalando Dependências
Bash
pip install pika
📚 Resumo Técnico dos Módulos
Abaixo estão os 6 padrões de mensageria implementados, evoluindo em complexidade.

1. Hello World (Básico)
O padrão mais simples de mensageria 1-para-1.

Arquivos: send.py (Produtor) e receive.py (Consumidor).

Conceito: O produtor envia uma mensagem para uma fila padrão (hello) e o consumidor a recebe.

Fluxo: P -> [Fila] -> C

2. Work Queues (Filas de Tarefas)
Distribuição de tarefas pesadas entre múltiplos trabalhadores (workers).

Conceito: Se rodarmos múltiplos consumidores, o RabbitMQ distribui as mensagens via Round-robin (um para cada, sequencialmente).

Aplicação: Útil para processamento de dados onde cada mensagem representa uma tarefa que demanda tempo.

3. Publish/Subscribe (Broadcast)
Envio de mensagens para múltiplos consumidores simultaneamente.

Arquivos: emit_log.py e receive_logs.py.

Exchange: Tipo fanout.

Conceito: O produtor manda para uma Exchange (não mais direto para a fila). A Exchange duplica a mensagem para todas as filas temporárias conectadas.

Aplicação: Sistemas de notificação onde um evento dispara múltiplas reações independentes.

4. Routing (Roteamento Direto)
Filtragem de mensagens baseada em critérios exatos.

Arquivos: emit_log_direct.py e receive_logs_direct.py.

Exchange: Tipo direct.

Conceito: Introdução da routing_key. O consumidor só recebe a mensagem se a chave da fila coincidir exatamente com a chave da mensagem (ex: error, info).

Aplicação: Separar logs críticos (salvar em disco) de logs informativos (apenas exibir).

5. Topics (Roteamento por Padrões)
Filtragem avançada baseada em padrões de texto (wildcards).

Arquivos: emit_log_topic.py e receive_logs_topic.py.

Exchange: Tipo topic.

Wildcards:

* (asterisco): Substitui exatamente uma palavra.

# (tralha): Substitui zero ou mais palavras.

Aplicação: Roteamento complexo, ex: kern.* (todos eventos de kernel) ou *.critical (todos eventos críticos).

6. RPC (Remote Procedure Call)
Simulação de chamadas síncronas (Request/Response) sobre uma arquitetura assíncrona.

Arquivos: rpc_server.py e rpc_client.py.

Mecânica:

Cliente envia mensagem definindo reply_to (fila de resposta) e correlation_id (ID único).

Servidor processa (ex: Fibonacci) e devolve o resultado na fila reply_to.

Cliente valida o correlation_id e consome a resposta.

Aplicação: Executar comandos em servidores remotos e aguardar o resultado, com buffer de carga.

▶️ Como Executar
Para ver os exemplos funcionando, abra dois ou mais terminais (Split Terminal no VS Code é recomendado).

Exemplo (Pub/Sub):

Terminal 1 (Consumidor):

Bash
python receive_logs.py
Terminal 2 (Produtor):

Bash
python emit_log.py "Mensagem de teste"
Estudo realizado em Janeiro/2026 como parte da formação em Engenharia de Dados.