import time

import requests


def local_server(login, password):
    data = {'login': login, 'password': password}
    response = requests.post('http://127.0.0.1:5000/auth', json=data)
    return response.status_code == 200


def local_server_protected(login, password, attempts=10, timeout=2):
    data = {'login': login, 'password': password}
    for i in range(attempts):
        try:
            response = requests.post('http://127.0.0.1:5000/auth', json=data)
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                return False
        except Exception as e:
            print("Connection Error!", e)

        if i < attempts - 1:
            time.sleep(timeout)

    print('Не удалось проверить пару', data)
    return False


def example_com(login, password):
    data = {'email': login, 'password': password}
    response = requests.post('http://127.0.0.1:5000/auth', json=data)
    return 'Неправильные данные для входа' not in response.text
