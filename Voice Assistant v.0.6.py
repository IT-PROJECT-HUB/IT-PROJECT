import pyttsx3
import speech_recognition as sr
import json
import random
import nltk

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split

from PyQt5 import QtWidgets, QtCore
import newinterface_ui

import threading


with open('NEW_BIG_BOT_CONFIG.json', 'r') as f:
    BOT_CONFIG = json.load(f)

work = True


class Assistant(QtWidgets.QMainWindow, newinterface_ui.Ui_MainWindow, threading.Thread):

    def __init__(self):
        super(Assistant, self).__init__()
        self.setupUi(self)
        self.r = sr.Recognizer()
        #####
        self.pushButton.pressed.connect(self.start_thread_assist)
        self.pushButton_2.pressed.connect(self.off)
        #####

    def cleaner(self, text):
        cleaned_text = ''
        for ch in text.lower():
            if ch in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz ':
                cleaned_text = cleaned_text + ch
        return cleaned_text

    def match(self, text, example):
        return nltk.edit_distance(text, example) / len(example) < 0.4 if len(example) > 0 else False

    def get_intent(self, text):
        for intent in BOT_CONFIG['intents']:
            if 'examples' in BOT_CONFIG['intents'][intent]:
                for example in BOT_CONFIG['intents'][intent]['examples']:
                    if self.match(self.cleaner(text), self.cleaner(example)):
                        return intent

    def ml_model(self, text):
        X = []
        y = []

        for intent in BOT_CONFIG['intents']:
            if 'examples' in BOT_CONFIG['intents'][intent]:
                X += BOT_CONFIG['intents'][intent]['examples']
                y += [intent for i in range(len(BOT_CONFIG['intents'][intent]['examples']))]

        # Создаем обучающую выборку для ML-модели

        vectorizer = CountVectorizer(preprocessor=self.cleaner, ngram_range=(1, 3), stop_words=['а', 'и'])
        # Создаем векторайзер – объект для превращения текста в вектора

        vectorizer.fit(X)
        X_vect = vectorizer.transform(X)
        # Обучаем векторайзер на нашей выборке

        X_train_vect, X_test_vect, y_train, y_test = train_test_split(X_vect, y, test_size=0.3)
        # Разбиваем выборку на train и на test

        # log_reg = LogisticRegression()
        # log_reg.fit(X_train_vect, y_train)
        # log_reg.score(X_test_vect, y_test)

        sgd = SGDClassifier()  # Создаем модель
        # sgd.fit(X_train_vect, y_train) # Обучаем модель
        # sgd.score(X_test_vect, y_test) # Проверяем качество модели на тестовой выборке
        sgd.fit(X_vect, y)

        sgd.score(X_vect, y)  # Смотрим качество классификации
        return sgd.predict(vectorizer.transform([text]))[0]

    def intenter(self, text):
        intent = self.get_intent(text)

        if intent is None:
            intent = self.ml_model(text)

        self.talk(random.choice(BOT_CONFIG['intents'][intent]['responses']))

    def talk(self, text):
        self.engine = pyttsx3.init(debug=True)
        print(text)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft)
        item.setText('MORGAN:' + '\n' + text)
        self.listWidget.addItem(item)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("Скажите что-нибудь...")
            self.r.adjust_for_ambient_noise(source)  # Этот метод нужен для автоматического понижени уровня шума
            audio = self.r.listen(source)
            try:
                text = self.r.recognize_google(audio, language="ru-RU").lower()
            except sr.UnknownValueError:
                pass
            print(text)
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignRight)
            item.setText('Вы сказали:' + '\n' + text)
            self.listWidget.addItem(item)
            return text

    def off(self):
        global work
        work = False

    def main(self):
        global work

        while work:
            try:
                self.intenter(self.listen())
            except:
                pass

    def start_thread_assist(self):
        thread = threading.Thread(target=self.main, args=())
        thread.start()


App = QtWidgets.QApplication([])
window = Assistant()
window.show()
App.exec()
