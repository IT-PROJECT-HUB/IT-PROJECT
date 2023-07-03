import weather_ui
from PyQt5 import QtWidgets
from pyowm import OWM
from pyowm.utils.config import get_default_config

class Weather(QtWidgets.QMainWindow, weather_ui.Ui_MainWindow):
    config_dict = get_default_config()  # Инициализация get_default_config()
    config_dict['language'] = 'ru'  # Установка языка

    def __init__(self):
        super(Weather, self).__init__()
        self.setupUi(self)

        self.pushButton.pressed.connect(self.go)

    def go(self):
        place = self.lineEdit.text()
        self.weather(place)

    def weather(self, place):
        owm = OWM('YOUR API KEY')  # Ваш ключ с сайта open weather map
        mgr = owm.weather_manager()  # Инициализация owm.weather_manager()
        observation = mgr.weather_at_place(place)
        # Инициализация mgr.weather_at_place() И передача в качестве параметра туда страну и город
        w = observation.weather

        status = w.detailed_status  # Узнаём статус погоды в городе и записываем в переменную status
        w.wind()  # Узнаем скорость ветра
        humidity = w.humidity  # Узнаём Влажность и записываем её в переменную humidity
        temp = w.temperature('celsius')[
            'temp']  # Узнаём температуру в градусах по цельсию и записываем в переменную temp
        print("В городе " + str(place) + " сейчас " + str(status) +  # Выводим город и статус погоды в нём
              "\nТемпература " + str(
            round(temp)) + " градусов по цельсию" +  # Выводим температуру с округлением в ближайшую сторону
              "\nВлажность составляет " + str(humidity) + "%" +  # Выводим влажность в виде строки
              "\nСкорость ветра " + str(w.wind()['speed']) + " метров в секунду")  # Узнаём и выводим скорость ветра

        self.label.setText("В городе " + str(place) + " сейчас " + str(status) +  # Выводим город и статус погоды в нём
              "\nТемпература " + str(
            round(temp)) + " градусов по цельсию" +  # Выводим температуру с округлением в ближайшую сторону
              "\nВлажность составляет " + str(humidity) + "%" +  # Выводим влажность в виде строки
              "\nСкорость ветра " + str(w.wind()['speed']) + " метров в секунду")


App = QtWidgets.QApplication([])
window = Weather()
window.show()
App.exec()
