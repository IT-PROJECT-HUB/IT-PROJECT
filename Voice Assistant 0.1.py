# Импорт всех необходимых модулей
import speech_recognition as sr # Модуль для прослушивания микрофона
import pyttsx3 # Модуль для воспроизведения текста в речь
from fuzzywuzzy import fuzz # Модуль для нечёткого распознавания речи
import datetime # Модуль для определения время
 
# Словарь со всеми настройками
main = {
    "name": ('морган', 'морг', 'моргэн', 'ладно'),
    "remove": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "time": ('текущее время', 'сейчас времени', 'который час')
    }
}
# Глобальные переменные
r = sr.Recognizer()
engine = pyttsx3.init()
text = ''
 
# Функции
 
 
def talk(speech):
    # Вывод сказанного текста на экран и озвучивание
    print(speech)
    engine.say(speech)
    engine.runAndWait()
 
 
def listen(): # Функция прослушивания микрофона и обработки запроса
    global text
    text = ''
    with sr.Microphone() as source:
        print("Скажите что-нибудь...")
        r.adjust_for_ambient_noise(source)  # Этот метод нужен для автоматического понижения уровня шума
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="ru-RU").lower()
            if text.startswith(main["name"]): # Проверка начинается ли фраза с имени Ассистента
                cmd = text
 
                for x in main['name']: # Вырезание имя Ассистента с запроса
                    cmd = cmd.replace(x, '').strip()
 
                for x in main["remove"]: # Вырезание слов с ячейки remove
                    cmd = cmd.replace(x, '').strip()
 
                # Распознаём и выполняем команду
                print(text)
                cmd = fuzzy_recognizer(cmd)
                func_cmds(cmd['cmd'])
        except sr.UnknownValueError:
            pass
        return text
 
 
def fuzzy_recognizer(cmd): # Функция нечёткого распознавания речи
    fr = {'cmd': '', 'percent': 50}
    for c, v in main["cmds"].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > fr['percent']:
                fr['cmd'] = c
                fr['percent'] = vrt
                func_cmds(fr)
    return fr
 
 
def func_cmds(cmd): # Функция со всеми имеющимися командами
    if cmd == "time":
        now = datetime.datetime.now()
        talk("Сейчас " + str(now.hour) + ":" + str(now.minute))
 
 
def main_func(): # Главная функция
    listen()
 
 
while True: # Бесконечный цикл
    main_func() # Вызов функции main_func()
 
