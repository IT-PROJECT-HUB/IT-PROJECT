import random
 
 
def hard_gen_pass(length=10):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphabet += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    choice = input("Хотите в пароле использовать цифры?(y/n): ")
    if choice == 'y' or choice == 'Y' or choice == 'Yes' or choice == 'yes':
        alphabet += '0123456789'
    choice = input("Хотите в пароле использовать cпец. символы?(y/n): ")
    if choice == 'y' or choice == 'Y' or choice == 'Yes' or choice == 'yes':
        alphabet += '!@#$%^&*()_+|?<>./,'
    password = ''
    for i in range(length):
        password += random.choice(alphabet)
    return password
 
 
ilength = input("Сколько символов должно быть в пароле: ")
result = hard_gen_pass(int(ilength))
print(result)
 
