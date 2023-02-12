import generators
import queries
import logics

#logics.simple_logic(
#    login_generator=generators.ListGenerator(tokens=['admin', 'jack', 'cat']),
#    password_generator=generators.FileGenerator(filename='pop_pass.txt'),
#    query=queries.local_server
#)  # Подбор пароля к определенному логину

#logics.get_accounts_logic(
#    login_generator=generators.FileGenerator(filename='pop_pass.txt'),
#    password_generator=generators.FileGenerator(filename='pop_pass.txt'),
#    query=queries.local_server
#)  # Подбор к топ 10000 популярных паролей логина из того же списка

#logics.get_accounts_logic(
#    login_generator=generators.ListGenerator(tokens=['admin', 'jack', 'cat']),
#    password_generator=generators.BruteForceGenerator(),
#    query=queries.local_server,
#    password_limit=1000000
#)  # Брут форс пароля к определенным логинам/логину

logics.get_password_logic(
    login_generator=generators.ListGenerator(tokens=['admin', 'jack', 'cat']),
    password_generator=generators.FileGenerator(filename='pop_pass.txt'),
    query=queries.local_server_protected
)  # Протестируйте сами и узнаете что это, ибо я сам хз :)
