import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Mudança: Tipo agora é 'topic'
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# Pega a chave de roteamento do primeiro argumento (ex: "kern.critical")
routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(
    exchange='topic_logs',
    routing_key=routing_key,
    body=message)

print(f" [x] Enviado '{routing_key}':'{message}'")
connection.close()