# install rabbitmq
```bash
docker run -d --hostname my-rabbit --name rabbitmq -p 5672:5672 -p 15672:15672  -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management
```

# install requirement
```bash
pip install -r requirements.txt
```

# start sever
```angular2html
python pull_data/send_pull_review_request.py
```