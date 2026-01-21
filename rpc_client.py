import pika
import uuid

class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))

        self.channel = self.connection.channel()

        # Cria fila temporária para receber as respostas
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        # Começa a escutar a fila de respostas
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        # Verifica se o ID da resposta bate com o da pergunta
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4()) # Gera ID único
        
        # Envia a pergunta
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, # "Responda aqui"
                correlation_id=self.corr_id,  # "Use este protocolo"
            ),
            body=str(n))
        
        # Loop "bloqueante": espera até self.response ter valor
        while self.response is None:
            self.connection.process_data_events()
            
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print(" [x] Solicitando fib(30)")
response = fibonacci_rpc.call(30)
print(f" [.] Resposta: {response}")