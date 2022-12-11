import random
import math


class RSA:

    @staticmethod
    def __is_prime(n):
        if n <= 1:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        i = 3
        while i <= math.sqrt(n):
            if n % i == 0:
                return False
            i += 2
        return True

    def __generate_prime(self, a=0, b=100):
        num = 0
        while self.__is_prime(num) is False:
            num = random.randint(a, b)
        return num

    @staticmethod
    def __gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    def key_gen(self):
        p = self.__generate_prime()
        q = self.__generate_prime()
        n = p * q

        phi = (p - 1) * (q - 1)
        e = random.randint(1, phi)
        g = self.__gcd(e, phi)

        while g != 1:
            e = random.randint(1, phi)
            g = self.__gcd(e, phi)

        d = pow(e, -1, phi)
        return (e, n), (d, n)

    @staticmethod
    def encrypt(message, primary_key):
        key, n = primary_key
        return [pow(ord(char), key, n) for char in message]

    @staticmethod
    def decrypt(ciphertext, primary_key):
        key, n = primary_key
        return ''.join([chr(pow(char, key, n)) for char in ciphertext])


if __name__ == '__main__':
    public, private = RSA().key_gen()
    print(f'Public key: {public}')
    print(f'Private key: {private}')

    encrypted_message = RSA().encrypt(input('Enter a message: '), public)

    print('Encrypted message:', ''.join(map(lambda x: str(x), encrypted_message)))
    print('Decrypted message:', RSA().decrypt(encrypted_message, private))
