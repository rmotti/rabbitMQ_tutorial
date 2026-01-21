import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    n = int(body)
    print(f" [.] fib({n})")
    
    response = fib(n)

    # Publica a resposta na fila que o cliente pediu (reply_to)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    
    # Confirma que processou
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Garante que o servidor não pegue mais de 1 tarefa por vez
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Aguardando requisições RPC")
channel.start_consuming()