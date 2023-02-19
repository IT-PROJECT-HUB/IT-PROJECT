from flask import Flask, request, abort
from time import time

app = Flask(__name__)
database = []
# Структура database
# {
# 'name': 'Имя',
# 'text': 'Текст сообщения.',
# 'time': Время когда отправлено сообщение
# },


@app.route("/")
def main():
    return "Hello User! <a href='/send'>Send</a> " \
           "<a href='/messages?after=0'>Messages</a> " \
           "<a href='/status'>Status</a> "


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'Messenger',
        'time': time(),
        'count_user': len(set(message['name'] for message in database))
    }


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json
    print(data)

    name = data['name']
    text = data['text']

    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)

    message = {
        'name': name,
        'text': text,
        'time': time()
    }

    database.append(message)

    return {'ok': True}


@app.route("/messages")
def get_message():
    try:
        after = float(request.args['after'])
    except Exception as ex:
        print(ex)
        return abort(400)
    messages = []

    for message in database:
        if message['time'] > after:
            messages.append(message)

    return {'messages': messages[:50]}


if __name__ == '__main__':
    app.run()
