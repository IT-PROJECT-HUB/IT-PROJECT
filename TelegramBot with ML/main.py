# Импортируем все необходимые модули
import nltk
import random
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
 
with open('NEW_BIG_BOT_CONFIG.json', 'r') as f:
    BOT_CONFIG = json.load(f)  # читаем json в переменную BOT_CONFIG
 
 
def cleaner(text):  # Функция очистки текста
    cleaned_text = ''
    for i in text.lower():
        if i in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz ':
            cleaned_text = cleaned_text + i
 
    return cleaned_text
 
 
def match(text, example):  # Функция сравнения текстов
    return nltk.edit_distance(text, example) / len(example) < 0.4 if len(example) > 0 else False
 
 
def get_intent(text):  # функция определения интента текста
    global intent
    for intent in BOT_CONFIG['intents']:
        if 'examples' in BOT_CONFIG['intents'][intent]:
            for example in BOT_CONFIG['intents'][intent]['examples']:
                if match(cleaner(text), cleaner(example)):
                    return intent
 
 
X = []
Y = []
 
 
for intent in BOT_CONFIG['intents']:
    if 'examples' in BOT_CONFIG['intents'][intent]:
        X += BOT_CONFIG['intents'][intent]['examples']
        Y += [intent for i in range(len(BOT_CONFIG['intents'][intent]['examples']))]
# Создаём обучающую выборку для ML - модели
 
vectorizer = CountVectorizer(preprocessor=cleaner, ngram_range=(1, 3), stop_words=['а', 'и'])
# Создаём векторайзер - обьект для превращения текста в вектор
 
vectorizer.fit(X)
X_vect = vectorizer.transform(X)
# Обучаем векторайзер на нашей выборке
 
X_train_vect, X_test_vect, Y_train, Y_test = train_test_split(X_vect, Y, test_size=0.3)
# Разбиваем выборку на train и test
 
sgd = SGDClassifier()  # Создаём модель
sgd.fit(X_vect, Y)
sgd.score(X_vect, Y)  # Смотрим качество классификации
 
 
def get_intent_model(text):  # Функция определяющая интент текста с помощью ML модели
    return sgd.predict(vectorizer.transform([text]))[0]
 
 
def bot(text):  # функция бота
    global intent
    intent = get_intent(text)  # Пытаемся понять намерение и сравнить по Левенштейну
 
    if intent is None:
        intent = get_intent_model(text)  # пытаемся понять намерение с помощью ML модели
 
    print(intent)
    return random.choice(BOT_CONFIG['intents'][intent]['responses'])
    # Возвращаем рандомный ответ из определённого интента из словаря responses
 
 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
 
logger = logging.getLogger(__name__)
 
 
def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Я Бот, Гений, PlayBoy, чтобы начать диалог со мной, напиши мне "Привет"!')
 
 
def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Меню /help')
 
 
def output(update: Update, _: CallbackContext) -> None:
    text = update.message.text
    print(text)
    update.message.reply_text(bot(text))
 
 
def main() -> None:
    updater = Updater("1634315175:AAHuik8wP3O9HvQak58Yth0iHyYU2STSfUQ")
    dispatcher = updater.dispatcher
 
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
 
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, output))
 
    updater.start_polling()
 
    updater.idle()
 
 
main()
