# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(570, 702)
        font = QtGui.QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 640, 461, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 61, 551, 561))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(480, 640, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(31)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(31)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(290, 20, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setObjectName("textEdit_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Messenger"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Введите сообщение..."))
        self.pushButton.setText(_translate("MainWindow", ">"))
        self.label.setText(_translate("MainWindow", "Messenger"))
        self.textEdit_2.setPlaceholderText(_translate("MainWindow", "Введите имя"))