import pika
import uuid
import sys


class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost'
            )
        )

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(
            queue='',
            exclusive=True
        )
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=str(n)
        )

        while self.response is None:
            self.connection.process_data_events()

        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

fib_number = sys.argv[1] if len(sys.argv) > 1 else 30
try:
    fib_number = int(fib_number)
except TypeError:
    fib_number = 30

print(" [x] Reqesting fib({fib_number})")
response = fibonacci_rpc.call(fib_number)
print(f" [.] Got {response}")
