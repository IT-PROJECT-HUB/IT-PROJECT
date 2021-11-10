import speech_recognition as sr
 
r = sr.Recognizer()
 
 
def listen():
    with sr.Microphone() as source:
        print("Скажите что-нибудь...")
        r.adjust_for_ambient_noise(source)  # Этот метод нужен для автоматического понижени уровня шума
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="ru-RU").lower()
        except sr.UnknownValueError:
            pass
        print(text)
        return text
 
 
listen()
