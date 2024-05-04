from publisher import publish_message


if __name__ == '__main__':
    data = [
        {"item_id": "88201679", "shop_id": "20493037179"},
        {"item_id": "15014358770", "shop_id": "285380605"},
        {"item_id": "18888184154", "shop_id": "285380605"},
        {"item_id": "6150798245", "shop_id": "285380605"},
        {"item_id": "19964640467", "shop_id": "285380605"},
    ]
    for i in data:
        result = publish_message(i.get("shop_id"), i.get("item_id"))
        print (result)
