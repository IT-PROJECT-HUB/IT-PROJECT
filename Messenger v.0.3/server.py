from flask import Flask, request, abort
from time import time
import pymysql

app = Flask(__name__)
database = []
# Структура database
# {
# 'name': 'Имя',
# 'text': 'Текст сообщения.',
# 'time': Время когда отправлено сообщение
# },

connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root',
    database='my_db',
    cursorclass=pymysql.cursors.DictCursor
)


@app.route("/")
def main():
    return "Hello User! <a href='/send'>Send</a> " \
           "<a href='/messages?after=0'>Messages</a> " \
           "<a href='/status'>Status</a> "


@app.route("/status")
def status():
    count_users = 0

    with connection.cursor() as sql:
        sql.execute("SELECT * FROM `users`")
        rows = sql.fetchtall()

        for row in rows:
            print(row)
            count_users += 1

    return {
        'status': True,
        'name': 'Messenger',
        'time': time(),
        'count_user': count_users
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

    return {'messages': messages[:50]}  # Возвращает последние 50 сообщений


@app.route("/registration", methods=['POST'])
def registration():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)

    if 'nickname' not in data or 'password' not in data:
        return abort(400)

    nickname = data['nickname']
    user_password = data['password']

    with connection.cursor() as sql:
        sql.execute("SELECT username FROM `users` WHERE username= %s", nickname)
        result = sql.fetchall()

        if len(result) == 0:
            sql.execute(f"INSERT INTO `users` VALUES('{0}', '{nickname}', '{user_password}')")
            connection.commit()
            return {'ok': True}
        else:
            return abort(400)


@app.route("/login", methods=['POST'])
def login():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)

    if 'nickname' not in data or 'password' not in data:
        return abort(400)

    user_nickname = data['nickname']
    user_password = data['password']

    with connection.cursor() as sql:
        sql.execute("SELECT username FROM `users` WHERE username = %s", user_nickname)
        result = sql.fetchall()

        if len(result) == 0:
            print(f"Аккаунт с ником {user_nickname} не найден!")
            return abort(400)

        sql.execute("SELECT username FROM `users` WHERE username = %s", user_nickname)
        nick = sql.fetchone()

        sql.execute("SELECT password FROM `users` WHERE username = %s", user_nickname)
        pasw = sql.fetchone()

    if nick['username'] == user_nickname and pasw['password'] == user_password:
        print(f"Вы успешно вошли в аккаунт {user_nickname}")
        return {"ok": True}
    else:
        print("Ошибка!")
        return abort(400)

if __name__ == '__main__':
    app.run()
