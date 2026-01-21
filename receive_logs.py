import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Garantimos que a exchange existe (caso o consumer rode antes do producer)
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # 1. Cria fila temporária e exclusiva
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # 2. Bind: Conecta a fila criada à exchange 'logs'
    channel.queue_bind(exchange='logs', queue=queue_name)

    print(' [*] Aguardando logs. Para sair pressione CTRL+C')

    def callback(ch, method, properties, body):
        print(f" [x] {body.decode()}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrompido')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)