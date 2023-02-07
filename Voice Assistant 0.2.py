import speech_recognition as sr
import pyttsx3
from fuzzywuzzy import fuzz
import datetime
import random
import sys
from os import system
from colorama import *
import webbrowser
 
 
ndel = ['морган', 'морген', 'морг', 'моргэн', 'ладно',
        'не могла бы ты', 'пожалуйста', 'текущее', 'сейчас']
 
 
commands = ['текущее время', 'сейчас времени', 'который час',
            'открой браузер', 'открой интернет', 'запусти браузер',
            'привет', 'добрый день', 'здравствуй',
            'пока', 'вырубись',
            'выключи компьютер', 'выруби компьютер', ]
 
 
r = sr.Recognizer()
engine = pyttsx3.init()
text = ''
j = 0
num_task = 0
 
 
def talk(speech):
    print(speech)
    engine.say(speech)
    engine.runAndWait()
 
 
def fuzzy_recognizer(rec):
    global j
    ans = ''
    for i in range(len(commands)):
        k = fuzz.ratio(rec, commands[i])
        if (k > 70) & (k > j):
            ans = commands[i]
            j = k
    return str(ans)
 
 
def clear_task():
    global text
    for i in ndel:
        text = text.replace(i, '').strip()
        text = text.replace('  ', ' ').strip()
 
 
def listen():
    global text
    text = ''
    with sr.Microphone() as source:
        print("Я вас слушаю...")
        r.adjust_for_ambient_noise(source)  # Этот метод нужен для автоматического понижени уровня шума
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="ru-RU").lower()
        except sr.UnknownValueError:
            pass
        # print(text)
        system('cls')
        clear_task()
        return text
 
 
def cmd_init():
    global text, num_task
    text = fuzzy_recognizer(text)
    print(text)
    if text in cmds:
        if (text != 'пока') & (text != 'привет') & (text != 'который час') & (text != 'сейчас времени')\
                & (text != 'сейчас времени') & (text != 'добрый день') & (text != 'здравствуй'):
            k = ['Секундочку', 'Сейчас сделаю', 'Уже выполняю']
            talk(random.choice(k))
        cmds[text]()
    elif text == '':
        print("Команда не распознана")
    num_task += 1
    if num_task % 10 == 0:
        talk('У вас будут еще задания?')
    engine.runAndWait()
    engine.stop()
 
 
def time():
    now = datetime.datetime.now()
    talk("Сейчас " + str(now.hour) + ":" + str(now.minute))
 
 
def open_brows():
    webbrowser.open('https://google.com')
    talk("Браузер открыт!")
 
 
def shut():  # выключает компьютер
    global text
    talk("Подтвердите действие!")
    text = listen()
    print(text)
    if (fuzz.ratio(text, 'подтвердить') > 60) or (fuzz.ratio(text, "подтверждаю") > 60):
        talk('Действие подтверждено')
        talk('До скорых встреч!')
        system('shutdown /s /f /t 10')
        quite()
    elif fuzz.ratio(text, 'отмена') > 60:
        talk("Действие не подтверждено")
    else:
        talk("Действие не подтверждено")
 
 
def hello():
    k = ['Привет, чем могу помочь?', 'Оу, здраствуйте', 'Приветствую']
    talk(random.choice(k))
 
 
def quite():
    x = ['Надеюсь мы скоро увидимся!', 'Рада была помочь', 'Я отключаюсь']
    talk(random.choice(x))
    engine.stop()
    system('cls')
    sys.exit(0)
 
 
cmds = {
    'текущее время': time, 'сейчас времени': time, 'который час': time,
    'открой браузер': open_brows, 'открой интернет': open_brows, 'запусти браузер': open_brows,
    'привет': hello, 'добрый день': hello, 'здравствуй': hello,
    'пока': quite, 'вырубись': quite,
    'выключи компьютер': shut, 'выруби компьютер': shut,
}
 
 
print(Fore.YELLOW + '', end='')
system('cls')
 
 
def main():
    global text, j
    try:
        listen()
        if text != '':
            cmd_init()
            j = 0
    except UnboundLocalError:
        pass
    except NameError:
        pass
    except TypeError:
        pass
 
 
while True:
    main()
