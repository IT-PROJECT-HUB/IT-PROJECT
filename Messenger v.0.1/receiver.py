import requests
from datetime import datetime
import time


def print_messages(messages):
    for message in messages:
        dt = datetime.fromtimestamp(message['time'])
        print(dt.strftime('%H:%M:%S'), message['name'])
        print(message['text'] + '\n')


after = 0

while True:
    response = requests.get(url='http://127.0.0.1:5000/messages',
                            params={'after': after})
    messages = response.json()['messages']
    if messages:
        print_messages(messages)
        after = messages[-1]['time']

    time.sleep(1)
