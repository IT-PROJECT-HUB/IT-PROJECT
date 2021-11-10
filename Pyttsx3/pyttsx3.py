import pyttsx3
 
engine = pyttsx3.init()
 
 
def talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()
 
 
program = True
 
while program:
    k = input("Введите текст ")
    if k != "пока":
        talk(k)
    if k == "пока":
        talk("До скорых встреч")
        program = False
 
