import pyttsx3
import speech_recognition as sr
import json
import random
import nltk

with open('NEW_BIG_BOT_CONFIG.json', 'r') as f:
    BOT_CONFIG = json.load(f)


class Assistant:

    def __init__(self):
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()

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

    def intenter(self, text):
        intent = self.get_intent(text)

        if intent is None:
            return "Извините, я вас не поняла!"

        self.talk(random.choice(BOT_CONFIG['intents'][intent]['responses']))

    def talk(self, text):
        print(text)
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
            return text

    def main(self):
        try:
            self.intenter(self.listen())
        except:
            pass


while True:
    Assistant().main()
