class BruteForceGenerator:
    def __init__(self, alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
        self.alphabet = alphabet
        self.base = len(self.alphabet)
        self.i = 0
        self.length = 0

    def reset(self):
        self.i = 0
        self.length = 0

    def generate(self):
        x = self.i
        result = ''
        while len(result) < self.length:
            rest = x % self.base
            x = x // self.base
            result = self.alphabet[rest] + result

        if result == self.alphabet[-1] * self.length:
            self.length += 1
            self.i = 0
        else:
            self.i += 1
        return result


class ListGenerator:

    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def reset(self):
        self.i = 0


    def generate(self):
        if self.i >= len(self.tokens):
            return

        token = self.tokens[self.i]
        self.i += 1
        return token


class FileGenerator(ListGenerator):

    def __init__(self, filename='pop_pass.txt'):
        with open(filename) as f:
            tokens = f.read().split('\n')

        super().__init__(tokens=tokens)
