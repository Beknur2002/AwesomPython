import pika

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    print("Connection successful!")
    connection.close()
except pika.exceptions.AMQPConnectionError:
    print("Failed to connect to RabbitMQ. Ensure RabbitMQ is running.")
