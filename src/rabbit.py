import pika

class RabbitMQClient:
    def __init__(self, host='a7f86e10c71304eb4b59ee728bc2a225-473937219.us-east-1.elb.amazonaws.com', queue='default'):
        self.host = host
        self.queue = queue
        self.credentials = pika.PlainCredentials('admin', 'adminpassword')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,port=5672,  credentials=self.credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def publish(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)
        print(f" [x] Sent '{message}'")

    def consume(self, callback):
        def on_message(channel, method, properties, body):
            callback(body)

        self.channel.basic_consume(queue=self.queue, on_message_callback=on_message, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.connection.close()

if __name__ == '__main__':
    client = RabbitMQClient()
    client.publish('Hello World!')
    client.consume(lambda message: print(f" [x] Received '{message}'"))
    client.close()