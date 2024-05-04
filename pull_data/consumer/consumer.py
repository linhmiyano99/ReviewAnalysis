from flask import Flask, request, jsonify
import pika
import json
import requests
import pandas as pd

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
        'cookie': 'SPC_F=0fZXLhe08QwkVW6MBOPVh1TnQCC0xdEW; REC_T_ID=c06ad525-6b2b-11ee-bebf-7eabafc9a9b5; SPC_CLIENTID=MGZaWExoZTA4UXdrmuggufjrtmnmapet; SC_DFP=EEZyBapkMQifQwqpVLgsqjDNvWwsBtnv; __LOCALE__null=VN; SPC_SI=DI8fZgAAAAB5OFpkQUdlcNSCKAEAAAAAYktxVTVRUWs=; SPC_SEC_SI=v1-ZlJINzJLQWp5Z0VnM2lITO8Hnv8PSAVawVgoDxgnILsWKEFhEmgRg4tLSKR/kxTsuFkqylJNKLhzMs2nUpr0RrS0iu2Fc7bH86iOTYLIyWE=; csrftoken=3H7vFat09vJh0BIBkhXplhv7ySik5Lqg; _sapid=2c3817a8228188cd925dee7963f004484d7f5dc0bc730f9809f661d2; _QPWSDCXHZQA=26406edc-3ceb-4c65-a3da-8cfc1e49c8d6; REC7iLP4Q=1929cec6-53a1-4691-b521-1450500ff9c2; shopee_webUnique_ccd=P7E7EBG5ZKzeBouh6MlSKQ%3D%3D%7C%2BBRJytOUXOsVdKLTnzU3B%2BLZvZpeBSEops%2B8vwlr8BLrp3KQbKBYWDFcL%2BtxBsg4SoHlkDEmF80%3D%7C19ER5TogqsfGWrid%7C08%7C3; ds=3cdbcfdeed7848157445927a948a85b8; SPC_EC=.UkpqbU5HOElYVVBzRDBrMffQxWPHA+Pf0j7nqj3S4qF5U4GQNoPctJXSQRM3qMBLn1NZk8JwvTRxaYKUiUH6Se5ogu1DIKP1gTu7cxAdIz/TrC+K9EFur9MP3vh4Uin9Z32jTNcZyC5PLn38UKd2549lZoWpXvetn1uMaoiHpR1rZRUXfjIcejGC21R+gSePW6UvLOBOE2Q9zOUZ3VR7oQ==; SPC_ST=.UkpqbU5HOElYVVBzRDBrMffQxWPHA+Pf0j7nqj3S4qF5U4GQNoPctJXSQRM3qMBLn1NZk8JwvTRxaYKUiUH6Se5ogu1DIKP1gTu7cxAdIz/TrC+K9EFur9MP3vh4Uin9Z32jTNcZyC5PLn38UKd2549lZoWpXvetn1uMaoiHpR1rZRUXfjIcejGC21R+gSePW6UvLOBOE2Q9zOUZ3VR7oQ==; SPC_U=44322985; SPC_R_T_IV=a0NSMHBweEE1VzlCUFJIaQ==; SPC_T_ID=zLQ8B4VXCguTr7ywDMSRK/OBNpfSTOH3WpjnaX4BewIf/5yeiqk70PjmaOuvPjleyI8Zz+08fg3PW2DL5ZEnoif/JmgMRX3qYoLYqc9CPAJzZaErQZlqOQo4fvVXXk5QqPAyRNf8Ik7XCnfqsUFzGrO4VREmnuXA8D16mRHF9ko=; SPC_T_IV=a0NSMHBweEE1VzlCUFJIaQ==; SPC_R_T_ID=zLQ8B4VXCguTr7ywDMSRK/OBNpfSTOH3WpjnaX4BewIf/5yeiqk70PjmaOuvPjleyI8Zz+08fg3PW2DL5ZEnoif/JmgMRX3qYoLYqc9CPAJzZaErQZlqOQo4fvVXXk5QqPAyRNf8Ik7XCnfqsUFzGrO4VREmnuXA8D16mRHF9ko=; SPC_IA=1; SPC_CDS_CHAT=57a86bb3-f07d-4c64-b5e1-ae64bf4f5761',
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
            print(f"process shop_id = {shop_id}, item_id = {item_id}")


            # https://shopee.vn/api/v2/item/get_ratings?itemid=20493037179&shopid=88201679
            url = f"https://shopee.vn/api/v2/item/get_ratings?itemid={item_id}&shopid={shop_id}"
            result = []

            try:
                sub_reviews = upload_shopee_review(url, shop_id, item_id)
                result.extend(sub_reviews)
            except:
                print(".")
            df = pd.DataFrame(result)
            df.to_csv(f"data/input/{shop_id}_{item_id}_2.csv")
            return f"data/input/{shop_id}_{item_id}_2.csv"

    except Exception as e:
        return str(e)
    return ""