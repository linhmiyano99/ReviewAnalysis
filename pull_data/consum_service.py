import datetime
import time
import sys

from consumer.consumer import consume_message


print("consumer ", sys.argv[1])
if __name__ == '__main__':
    while True:
        time.sleep(10)
        print("time", datetime.datetime.now().time())
        a = consume_message()
        print("output", a)

