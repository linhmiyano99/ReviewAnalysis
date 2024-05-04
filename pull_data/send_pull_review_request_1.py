from flask import Flask, request, jsonify
import pika
import json
import requests
import pandas as pd
app = Flask(__name__)

# RabbitMQ credentials
rabbitmq_username = 'user'
rabbitmq_password = 'password'
rabbitmq_host = 'localhost'
rabbitmq_port = 5672

def upload_shopee_review(url, shop_id, item_id):
    payload = {}
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://shopee.vn/api/v2/item/get_ratings?itemid=20493037179&shopid=88201679',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    review_data = response.json()
    result = []
    for rating in review_data["data"]["ratings"]:
        review = {
            "reviewText": rating["comment"],
            "rate": rating["rating"],
            "orderId": rating["orderid"],
        }
        result.append(review)

    return result

@app.route('/api/publish', methods=['POST'])
def publish_message():
    try:

        # Get message body from request
        message_body = request.data.decode()

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

        return jsonify({'status': 'Message published successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/consume', methods=['GET'])
def consume_message():
    try:

        # Create connection to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port,
                                      credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password)))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue='shop-review-1', durable=True)

        # Get a single message from the queue
        method_frame, header_frame, body = channel.basic_get(queue='shop-review-1', auto_ack=True)

        if method_frame:
            message = json.loads(body.decode())
            shop_id = message.get('shop_id')
            item_id = message.get('item_id')


            # https://shopee.vn/api/v2/item/get_ratings?itemid=20493037179&shopid=88201679
            result = []

            sub_reviews = [""]
            try:
                while len(sub_reviews) != 0 and len(result) < 100:
                    url = f"https://shopee.vn/api/v2/item/get_ratings?itemid={item_id}&shopid={shop_id}&offset={len(sub_reviews)}"
                    sub_reviews = upload_shopee_review(url, shop_id, item_id)
                    result.extend(sub_reviews)
            except:
                print(".")
            df = pd.DataFrame(result)
            df.to_csv(f"data/input/{shop_id}_{item_id}.csv")
            return jsonify({'message': f"{len(result)} review"})
        else:
            return jsonify({'message': 'No messages in queue'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5001)
