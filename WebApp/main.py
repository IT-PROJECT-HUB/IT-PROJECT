import eel
from pyowm import OWM
from pyowm.utils.config import get_default_config
from config import TOKEN

config_dict = get_default_config()
config_dict['language'] = "ru"
owm = OWM(TOKEN)
mgr = owm.weather_manager()


@eel.expose
def weather(place):
    if place == "":
        return "Введите город"

    observation = mgr.weather_at_place(place)
    w = observation.weather

    status = w.detailed_status
    w.wind()
    humidity = w.humidity
    temp = w.temperature('celsius')['temp']

    return f"В городе {place} сейчас {status}\nТемпература {round(temp)} градусов по цельсию\n" \
           f"Влажность составляет {humidity}%\n Скорость ветра {w.wind()['speed']} метров в секунду"


eel.init("web")
eel.start("index.html", size=(400, 600))
