# Voice Assistant 0.8
import pyttsx3
import speech_recognition as sr
import colorama
from fuzzywuzzy import fuzz
import datetime
from os import system
import sys
from random import choice
from pyowm import OWM
from pyowm.utils.config import get_default_config
import webbrowser
import configparser
from psutil import virtual_memory as memory
import nltk
import json
import wikipedia as wiki
import re
import requests
from bs4 import BeautifulSoup
from forex_python.converter import CurrencyRates

with open('NEW_BIG_BOT_CONFIG.json', 'r') as f:
    BOT_CONFIG = json.load(f)


class Assistant:
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    config_dict = get_default_config()  # Инициализация get_default_config()
    config_dict['language'] = 'ru'  # Установка языка

    def __init__(self):
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        self.text = ''

        self.cmds = {
            ('текущее время', 'сейчас времени', 'который час'): self.time,
            ('привет', 'добрый день', 'здравствуй'): self.hello,
            ('пока', 'вырубись'): self.quite,
            ('выключи компьютер', 'выруби компьютер'): self.shut,
            ('какая погода', 'погода', 'погода на улице'): self.weather,
            ('добавить задачу', 'добавить заметку', 'создай заметку', 'создай задачу'): self.task_planner,
            ('список задач', 'список заметок', 'задачи', 'заметки'): self.task_list,
            ('загруженость компьютера', 'загруженость системы', 'загруженость',
             'состояние системы', 'какая загрузка системы', 'какая загрузка'): self.check_memory,
            ('включи музыку', 'вруби музон', 'вруби музыку', 'включи музон', 'врубай музыку'): self.music,
            ('расскажи анекдот', 'анекдот', 'пошути'): self.joke,
            ('какой курс валют', 'скажи курс валют', 'курс валют'): self.currency,
        }

        self.ndels = ['морган', 'морген', 'моргэн', 'морг', 'ладно', 'не могла бы ты', 'пожалуйста',
                      'текущее', 'сейчас']

        self.commands = [
            'текущее время', 'сейчас времени', 'который час',
            'открой браузер', 'открой интернет', 'запусти браузер',
            'привет', 'добрый день', 'здравствуй',
            'пока', 'вырубись',
            'выключи компьютер', 'выруби компьютер',
            'какая погода', 'погода', 'погода на улице', 'какая погода на улице',
            'добавить задачу', 'добавить заметку', 'создай заметку', 'создай задачу'
                                                                     'список задач', 'список заметок', 'задачи',
            'заметки',
            'загруженость компьютера', 'загруженость системы', 'какая загрузка',
            'включи музыку', 'вруби музон', 'вруби музыку', 'включи музон', 'врубай музыку',
            'расскажи анекдот', 'анекдот', 'пошути'
        ]

        self.num_task = 0
        self.j = 0
        self.ans = ''

        wiki.set_lang('ru')

    def cleaner(self, text):
        self.text = text

        for i in self.ndels:
            self.text = self.text.replace(i, '').strip()
            self.text = self.text.replace('  ', ' ').strip()

        self.ans = self.text

        for i in range(len(self.commands)):
            k = fuzz.ratio(text, self.commands[i])
            if (k > 70) & (k > self.j):
                self.ans = self.commands[i]
                self.j = k

        return str(self.ans)

    def check_memory(self):
        mem = memory()
        self.talk(f'Компьютер загружен на {round(mem.percent)}%')

    def intent_cleaner(self, text):
        cleaned_text = ''
        for i in text.lower():
            if i in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz ':
                cleaned_text += i
        return cleaned_text

    def match(self, text, example):
        return nltk.edit_distance(text, example) / len(example) < 0.4 if len(example) > 0 else False

    def get_intent(self, text):
        for intent in BOT_CONFIG['intents']:
            if 'examples' in BOT_CONFIG['intents'][intent]:
                for example in BOT_CONFIG['intents'][intent]['examples']:
                    if self.match(self.intent_cleaner(text), self.intent_cleaner(example)):
                        return intent

    def intenter(self, text):
        intent = self.get_intent(text)

        if intent is None:
            return

        self.talk(choice(BOT_CONFIG['intents'][intent]['responses']))

    def task_planner(self):
        self.talk("Что добавить в список задач?")
        task = self.listen()

        with open('TODO_LIST.txt', 'a') as file:
            file.write(f'{task}\n')

        self.talk(f'Задача {task} добавлена в список задач!')

    def task_list(self):
        with open('TODO_LIST.txt', 'r') as file:
            tasks = file.read()
        self.talk(f"Список задач:\n{tasks}")

    def wiki_search(self, task):
        try:
            info = wiki.summary(task, sentences=3)
            self.talk((info.replace('англ', '')).replace('род.', 'родился').replace('(.', '').replace(')', '')
                      .replace(';', '').replace("(урожд. —", "").replace("урожд.", "").replace("  ", " "))
        except wiki.exceptions.PageError:
            pass
        except wiki.exceptions.WikipediaException:
            pass

    def music(self):
        self.talk(choice(['Приятного прослушивания!', 'Наслаждайтесь!', 'Приятного прослушивания музыки']))
        music_list = ['https://www.youtube.com/watch?v=IjwBMrxlOOA', 'https://www.youtube.com/watch?v=qj3-riPaHx8',
                      'https://www.youtube.com/watch?v=8-_4pilz70c', 'https://www.youtube.com/watch?v=ebfboqfPYGk']
        webbrowser.open(choice(music_list))

    def translate(self, task):
        self.talk(choice(['Сейчас попытаюсь перевести', 'Сейчас переведу', 'Сейчас попробую перевести']))
        variants = ['переведи', 'перевести', 'перевод', 'перевести', 'переводить']
        for i in variants:
            print(i)
            task = task.replace(i, '').replace('  ', ' ')
        print(task)
        webbrowser.open(f'https://translate.google.com/#view=home&op=translate&sl=auto&tl=ru&text={task}')

    def search_on_map(self, task):
        for j in ('найди на карте', 'найти на карте', 'поищи на карте'):
            task = task.replace(j, '').replace('  ', ' ').strip()
            for i in ['находится', 'расположен', 'где']:
                for k in ['мне', 'нам', 'всем', 'им']:
                    if fuzz.ratio(task.split()[0], i) > 70 or fuzz.ratio(task.split()[0], k) > 70:
                        task = ' '.join(task.split()[1:])
                    task = task.replace(i, '').replace(k, '').replace('  ', ' ').strip()
        webbrowser.open(f'https://google.com/maps/search/{task}')
        self.talk(choice(['Сейчас всё найду', 'Ищу на карте', 'Уже ищу']))

    def web_search(self, search):
        words = ['найди', 'найти', 'ищи', 'кто такой', 'что такое']
        remove = ["пожалуйста", "ладно", "давай", "сейчас"]
        for i in words:
            search = search.replace(i, '')
            for j in remove:
                search = search.replace(j, '')
                search = search.strip()
        self.talk(f"Ищу {search}")
        webbrowser.open(f'https://www.google.com/search?q={search}&oq={search}'
                        f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')

        self.wiki_search(search)

    def recognizer(self):
        self.text = self.cleaner(self.listen())
        print(self.text)

        if self.text.startswith(('открой', 'запусти', 'зайди', 'зайди на')):
            self.opener(self.text)

        elif self.text.startswith(('найди на карте', 'найти на карте', 'поищи на карте')):
            self.search_on_map(self.text)

        elif self.text.startswith(('найди', 'найти', 'ищи', 'кто такой', 'что такое')):
            self.web_search(self.text)

        elif self.text.startswith(('переведи', 'перевести', 'перевод', 'перевести', 'переводить')):
            self.translate(self.text)

        for tasks in self.cmds:
            for task in tasks:
                if fuzz.ratio(task, self.text) >= 80:
                    self.cmds[tasks]()
                    return

        self.intenter(self.text)

    def currency(self):
        self.talk(f'Курс доллара к Евро: {(CurrencyRates().get_rate("USD", "EUR")):2f}')

    def joke(self):
        link = requests.get('http://anekdotme.ru/random')
        parse = BeautifulSoup(link.text, "html.parser")
        select = parse.select('.anekdot_text')
        get = (select[0].getText().strip())
        reg = re.compile('[^a-zA-Zа-яА-я ^0-1-2-3-4-5-6-7-8-9:.,!?-]')
        joke = reg.sub('', get)
        self.talk(joke)

    def time(self):
        now = datetime.datetime.now()
        self.talk(f"Сейчас {now.hour} : {now.minute}")

    def opener(self, task):
        links = {
            ('youtube', 'ютуб', 'ютюб'): 'https://youtube.com/',
            ('вк', 'вконтакте', 'контакт', 'vk'): 'https:vk.com/feed',
            ('браузер', 'интернет', 'browser'): 'https://google.com/',
            ('insta', 'instagram', 'инста', 'инсту'): 'https://www.instagram.com/',
            ('почта', 'почту', 'gmail', 'гмейл', 'гмеил', 'гмаил'): 'http://gmail.com/',
        }
        j = 0
        if 'и' in task:
            task = task.replace('и', '').replace('  ', ' ')
        double_task = task.split()
        if j != len(double_task):
            for i in range(len(double_task)):
                for vals in links:
                    for word in vals:
                        if fuzz.ratio(word, double_task[i]) > 75:
                            webbrowser.open(links[vals])
                            self.talk('Открываю ' + double_task[i])
                            j += 1
                            break

    def cfile(self):
        try:
            cfr = Assistant.settings['SETTINGS']['fr']
            if cfr != 1:
                file = open('settings.ini', 'w', encoding='UTF-8')
                file.write('[SETTINGS]\ncountry = UA\nplace = Kharkov\nfr = 1')
                file.close()
        except Exception as e:
            print('Перезапустите Ассистента!', e)
            file = open('settings.ini', 'w', encoding='UTF-8')
            file.write('[SETTINGS]\ncountry = UA\nplace = Kharkov\nfr = 1')
            file.close()

    def quite(self):
        self.talk(choice(['Надеюсь мы скоро увидимся', 'Рада была помочь', 'Пока пока', 'Я отключаюсь']))
        self.engine.stop()
        system('cls')
        sys.exit(0)

    def shut(self):
        self.talk("Подтвердите действие!")
        text = self.listen()
        print(text)
        if (fuzz.ratio(text, 'подтвердить') > 60) or (fuzz.ratio(text, "подтверждаю") > 60):
            self.talk('Действие подтверждено')
            self.talk('До скорых встреч!')
            system('shutdown /s /f /t 10')
            self.quite()
        elif fuzz.ratio(text, 'отмена') > 60:
            self.talk("Действие не подтверждено")
        else:
            self.talk("Действие не подтверждено")

    def hello(self):
        self.talk(choice(['Привет, чем могу помочь?', 'Здраствуйте', 'Приветствую']))

    def weather(self):
        place = Assistant.settings['SETTINGS']['place']
        country = Assistant.settings['SETTINGS']['country']  # Переменная для записи страны/кода страны
        country_and_place = place + ", " + country  # Запись города и страны в одну переменную через запятую
        owm = OWM('fd5321547e631b45b33d6d1cc673754f')  # Ваш ключ с сайта open weather map
        mgr = owm.weather_manager()  # Инициализация owm.weather_manager()
        observation = mgr.weather_at_place(country_and_place)
        # Инициализация mgr.weather_at_place() И передача в качестве параметра туда страну и город

        w = observation.weather

        status = w.detailed_status  # Узнаём статус погоды в городе и записываем в переменную status
        w.wind()  # Узнаем скорость ветра
        humidity = w.humidity  # Узнаём Влажность и записываем её в переменную humidity
        temp = w.temperature('celsius')[
            'temp']  # Узнаём температуру в градусах по цельсию и записываем в переменную temp
        self.talk("В городе " + str(place) + " сейчас " + str(status) +  # Выводим город и статус погоды в нём
                  "\nТемпература " + str(
            round(temp)) + " градусов по цельсию" +  # Выводим температуру с округлением в ближайшую сторону
                  "\nВлажность составляет " + str(humidity) + "%" +  # Выводим влажность в виде строки
                  "\nСкорость ветра " + str(w.wind()['speed']) + " метров в секунду")  # Узнаём и выводим скорость ветра

    def talk(self, text):
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.stop()

    def listen(self):
        with sr.Microphone() as source:
            print(f"{colorama.Fore.LIGHTGREEN_EX}Я вас слушаю...")
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
            try:
                self.text = self.r.recognize_google(audio, language="ru-RU").lower()
            except Exception as e:
                print(e)
            return self.text


Assistant().cfile()
Assistant().hello()

while True:
    try:
        Assistant().recognizer()
    except Exception as ex:
        print(ex)
