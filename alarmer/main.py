import datefinder
import winsound
import datetime


def alarm(text):
    time = datefinder.find_dates(text)
    date_and_time = ''
    for date_and_time in time:
        print(date_and_time)
    date_time = str(date_and_time)
    only_time = date_time[11:]
    print(only_time)
    hour_time = int(only_time[:-6])
    min_time = int(only_time[3:-3])

    while True:
        if hour_time == datetime.datetime.now().hour:
            if min_time == datetime.datetime.now().minute:
                print('Будильник сработал!')
                winsound.PlaySound('sound.wav', winsound.SND_LOOP)
            elif min_time <= datetime.datetime.now().minute:
                break
            else:
                pass
        else:
            pass


alarm('16:22')
