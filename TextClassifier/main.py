from sklearn.feature_extraction.text import TfidfVectorizer  # skleran для классификации текста
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from Stemmer import Stemmer  # Stemmer нужен для приведения слов к начальной форме
import numpy as np  # numpy для работы с массивами
import sys
import re  # регулярные выражения для очистки текста


def load():
    data = {'intent': [], 'response': []}  # словарь для хранения данных

    with open("model.txt", "r", encoding="utf-8") as file:  # открываем файл с данными
        for line in file:  # читаем файл построчно
            row = line.split("|")  # разбиваем строку на массив
            data['intent'] += [row[0]]  # добавляем вопрос в словарь
            data['response'] += [row[1]]  # добавляем ответ в словарь

    return data


def cleaner(text):
    text = text.lower()
    stemmer = Stemmer("russian")  # создаем экземпляр класса Stemmer для русского языка
    text = " ".join(stemmer.stemWords(text.split()))  # применяем стемминг к тексту (приводим слова к начальной форме)
    text = re.sub(r'\b\d+\b', ' digit ', text)  # заменяем числа на слово digit
    return text


def train_test_split(data, validation_split=0.2):  # функция разбиения выборки на обучающую и тестовую. validation_split - доля тестовой выборки
    size = len(data['intent'])  # размер выборки
    indices = np.arange(size)  # создаем массив индексов
    np.random.shuffle(indices)  # перемешиваем массив индексов

    x = [data['intent'][i] for i in indices]  # создание массива из текстов
    y = [data['response'][i] for i in indices]  # создание массива из ответов
    validation_samples = int(validation_split * size)  # определяем размер валидационной выборки

    return {
        'train': {'x': x[:-validation_samples], 'y': y[:-validation_samples]},  # обучающая выборка
        'test': {'x': x[-validation_samples:], 'y': y[-validation_samples:]}  # тестовая выборка
    }


def model():
    data = load()  # загружаем данные
    sample = train_test_split(data)  # разбиваем выборку на обучающую и тестовую
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),  # tfidf векторизация текста (преобразование текста в вектор)
        ('clf', SGDClassifier(loss='hinge'))  # классификатор (метод опорных векторов) с функцией потерь hinge нужен для классификации текста
    ])  # создаем модель

    pipeline.fit(sample['train']['x'], sample['train']['y'])  # обучаем модель
    predicted = pipeline.predict(sample['train']['x'])  # предсказываем результаты обучающей выборки
    print(np.mean(predicted == sample['train']['y']))  # считаем точность обучающей выборки

    while True:
        intent = input(">>> ").replace("?", "").strip()
        intents = [intent]
        predicted = pipeline.predict(intents)  # предсказываем результаты тестовой выборки
        print(predicted[0].strip())  # выводим результат


if __name__ == '__main__':
    sys.exit(model())
