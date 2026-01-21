import pika

# 1. Estabelece conexão com o RabbitMQ (localhost)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Cria a fila chamada 'hello'. 
# (É boa prática declarar a fila aqui para garantir que ela exista)
channel.queue_declare(queue='hello')

# 3. Envia a mensagem para a fila 'hello'
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Olá, RabbitMQ!')

print(" [x] Mensagem enviada!")

connection.close()