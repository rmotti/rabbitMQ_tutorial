import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 1. Declaramos a Exchange do tipo 'fanout' (espalha para todos)
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Pega mensagem do terminal ou usa padrão
message = ' '.join(sys.argv[1:]) or "info: Hello World!"

# 2. Publicamos na Exchange 'logs'. 
# A routing_key é vazia ('') porque fanout ignora isso.
channel.basic_publish(exchange='logs', routing_key='', body=message)

print(f" [x] Enviado: {message}")
connection.close()