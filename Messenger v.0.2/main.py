import interface
from PyQt5 import QtWidgets, QtCore
import requests
from datetime import datetime


class Messenger(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self):
        super(Messenger, self).__init__()
        self.setupUi(self)
        self.after = 0
        self.pushButton.clicked.connect(self.send_message)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    def show_messages(self, message):
        item = QtWidgets.QListWidgetItem()
        dt = datetime.fromtimestamp(message['time'])
        item.setText(f"{message['name']} {dt.strftime('%H:%M')}\n{message['text']}")
        self.listWidget.addItem(item)

    def get_messages(self):
        try:
            response = requests.get(url='http://127.0.0.1:5000/messages', params={'after': self.after})
        except Exception as e:
            print(e)
            return
        messages = response.json()['messages']
        for i in range(len(messages)):
            self.show_messages(messages[i])
            self.after = messages[i]['time']
            self.listWidget.scrollToBottom()

    def send_message(self):
        name = self.textEdit_2.toPlainText()
        text = self.textEdit.toPlainText()
        if len(name) > 0 and len(text) > 0:
            try:
                response = requests.post(url='http://127.0.0.1:5000/send', json={'name': name, 'text': text})
            except Exception as e:
                item = QtWidgets.QListWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setText('Сервер недоступен!\n')
                self.listWidget.addItem(item)
                print(e)
                return

            if response.status_code != 200:
                item = QtWidgets.QListWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setText('Неправильное имя или текст!\n')
                self.listWidget.addItem(item)
                return

            self.textEdit.clear()


if __name__ == '__main__':
    App = QtWidgets.QApplication([])
    window = Messenger()
    window.show()
    App.exec()
