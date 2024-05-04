from flask import Flask, request, jsonify
import pika
import json
app = Flask(__name__)

# RabbitMQ credentials
rabbitmq_username = 'user'
rabbitmq_password = 'password'
rabbitmq_host = 'localhost'
rabbitmq_port = 5672

def publish_message(shop_id, item_id):
    try:
        data = {
            "shop_id": shop_id,
            "item_id":item_id
        }
        # Get message body from request
        message_body = json.dumps(data)

        # Create connection to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port,
                                      credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password)))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue='shop-review-1', durable=True)

        # Publish message to the queue
        channel.basic_publish(exchange='shop', routing_key='shop-review-1', body=message_body)

        # Close connection
        connection.close()

        return 'Message published successfully'

    except Exception as e:
        return f"'error': {str(e)}"
