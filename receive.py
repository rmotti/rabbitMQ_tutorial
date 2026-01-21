import pika, sys, os

def main():
    # Conexão igual ao anterior
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declara a fila novamente (para garantir que funciona mesmo se rodar o consumer antes do producer)
    channel.queue_declare(queue='hello')

    # Função de callback: o que fazer quando uma mensagem chegar?
    def callback(ch, method, properties, body):
        print(f" [x] Recebido: {body.decode()}")

    # Diz ao RabbitMQ para usar a função 'callback' quando chegarem mensagens na fila 'hello'
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Aguardando mensagens. Para sair pressione CTRL+C')
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