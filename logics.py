def simple_logic(login_generator, password_generator, query):
    login = login_generator.generate()
    if login is None:
        return

    while True:
        password = password_generator.generate()
        if password is None:
            return

        if query(login, password):
            print('SUCCESS', login, password)
            return


def get_accounts_logic(login_generator, password_generator, query, login_limit=1000, password_limit=1000):
    success_logins = set()

    for i in range(password_limit):
        password = password_generator.generate()
        if password is None:
            return

        login_generator.reset()
        for j in range(login_limit):
            login = login_generator.generate()
            if login is None:
                break

            if login not in success_logins and query(login, password):
                print('SUCCESS', 'LOGIN:', login, 'PASSWORD:', password)
                success_logins.add(login)


def get_password_logic(login_generator, password_generator, query, password_limit=1000):
    while True:
        login = login_generator.generate()
        if login is None:
            break

        password_generator.reset()
        for j in range(password_limit):
            password = password_generator.generate()
            if password is None:
                break

            if query(login. password):
                print('SUCCESS', login, password)
                break
