import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Mudança 1: Tipo da exchange agora é 'direct'
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Pega a severidade dos argumentos (padrão 'info')
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

# Mudança 2: Publicamos com uma routing_key específica
channel.basic_publish(
    exchange='direct_logs',
    routing_key=severity,
    body=message)

print(f" [x] Enviado '{severity}':'{message}'")
connection.close()