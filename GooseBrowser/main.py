from PyQt5.QtWebEngineWidgets import *  # pip install pyqtwebengine
from PyQt5.QtWidgets import QShortcut  # pip install pyqt5
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tab_widget)

        self.tab_widget.setStyleSheet("""
            QTabBar{
                background: #f0f0f0;
            }
            QTabBar::tab{
                background: #fff;
                color: #0f0f0f;
                height: 22px;
                margin-left: 5px;
            }
            QTabBar::tab:selected{
                content: "|";
            }
            QTabBar::tab:selected{
                background-color: #b3b3b3;
                color: #000000;
                padding-left: 5px;
                padding-right: 5px;
                border: 1px solid #9e9e9e;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border-bottom-left-radius: -4px;
                border-bottom-right-radius: -4px;
            }
            QTabBar::close-button{
                image: url("images/close.png");
                subcontrol-position: right;
            }
            QLabel{
                background-color: #23272a;
                font-size: 22px;
                padding-left: 5px;
                color: #fff;
            }
        """)

        qtoolbar = QToolBar("Nav")
        qtoolbar.setIconSize(QSize(30, 30))
        qtoolbar.setAllowedAreas(Qt.TopToolBarArea)
        qtoolbar.setFloatable(False)
        qtoolbar.setMovable(False)
        self.addToolBar(qtoolbar)

        qtoolbar.setStyleSheet("""
            QToolButton{
                border: 2px;
                padding: 1px 4px;
                background: transparent;
                border-radius: 4px;
            }
            QTollButton:hover{
                border: 1px;
                background: #c3c3c3;
            }
            QToolButton:selected{
                background: #a8a8a8;
            }
            QToolButton:pressed{
                background: #888888;
            }
        """)

        back_btn = QAction(QIcon(os.path.join("images", "back.png")), "Назад", self)
        back_btn.setStatusTip("Вернуться на предыдущую страницу")
        back_btn.triggered.connect(lambda: self.tab_widget.currentWidget().back())
        qtoolbar.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join("images", "forward.png")), "Вперёд", self)
        next_btn.setStatusTip("Перейти на страницу вперёд")
        next_btn.triggered.connect(lambda: self.tab_widget.currentWidget().forward())
        qtoolbar.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join("images", "reload.png")), "Обновить страницу", self)
        reload_btn.setStatusTip("Перезагрузить страницу")
        reload_btn.triggered.connect(lambda: self.tab_widget.currentWidget().reload())
        qtoolbar.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join("images", "home.png")), "Домой", self)
        home_btn.setStatusTip("Домой")
        home_btn.triggered.connect(lambda: self.nav_home())
        qtoolbar.addAction(home_btn)

        qtoolbar.addSeparator()

        self.https_icon = QLabel()
        self.https_icon.setPixmap(QPixmap(os.path.join("images", "lock.png")))
        qtoolbar.addWidget(self.https_icon)

        self.url_line = QLineEdit()
        self.url_line.returnPressed.connect(self.nav_to_url)
        qtoolbar.addWidget(self.url_line)

        new_tab_btn = QAction(QIcon(os.path.join("images", "add-icon.png")), "Новая вкладка", self)
        new_tab_btn.setStatusTip("Открыть новую вкладку")
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        qtoolbar.addAction(new_tab_btn)

        info_btn = QAction(QIcon(os.path.join("images", "info.png")), "Информация", self)
        info_btn.triggered.connect(self.info)
        qtoolbar.addAction(info_btn)

        self.url_line.setStyleSheet("""
            border: 1px;
            border-radius: 10px;
            padding: 3;
            background: #fff;
            selection-background-color: darkgray;
            left:5px;
            right: 5px;
            font: 12px/14px sans serif;
        """)

        self.add_new_tab(QUrl("https://google.com"), "Домашняя страница")

        self.shortcut = QShortcut(QKeySequence("F5"), self)
        self.shortcut.activated.connect(lambda: self.tab_widget.currentWidget().reload())

        self.show()
        self.setWindowIcon(QIcon(os.path.join("images", "goose-icon.png")))

    def add_new_tab(self, qurl=QUrl("https://google.com"), label="blank"):
        browser = QWebEngineView()
        browser.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        browser.page().fullScreenRequested.connect(lambda request: request.accept())
        browser.setUrl(qurl)

        tab = self.tab_widget.addTab(browser, label)
        self.tab_widget.setCurrentIndex(tab)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=tab, browser=browser:
                                     self.tab_widget.setTabText(tab, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tab_widget.currentWidget().url()
        self.update_urlbar(qurl, self.tab_widget.currentWidget())
        self.update_title(self.tab_widget.currentWidget())

    def close_current_tab(self, i):
        if self.tab_widget.count() < 2:
            return

        self.tab_widget.removeTab(i)

    def update_title(self, browser):
        if browser != self.tab_widget.currentWidget():
            return
        title = self.tab_widget.current().page().title()
        self.setWindowTitle(f"{title} - Goose Browser")

    def info(self):
        QMessageBox.about(self, "Goose Browser", "Самый лучший браузер в мире!\nСоздан by Neor")

    def nav_home(self):
        self.tab_widget.currentWidget().setUrl(QUrl("https://google.com"))

    def nav_to_url(self):
        qurl = QUrl(self.url_line.text())
        if qurl.scheme() == "":
            qurl.setScheme("http")

        self.tab_widget.currentWidget().setUrl(qurl)

    def update_urlbar(self, url, browser=None):
        if browser != self.tab_widget.currentWidget():
            return

        if url.scheme() == "https":
            self.https_icon.setPixmap(QPixmap(os.path.join("images", "lock.png")))
        else:
            self.https_icon.setPixmap(QPixmap(os.path.join("images", "unlock.png")))

        self.url_line.setText(url.toString())
        self.url_line.setCursorPosition(999)



if __name__ == '__main__':
    app = QApplication([])
    QApplication.setApplicationName("Goose Browser")
    app.setOrganizationName("IT Project")
    window = Browser()
    window.showMaximized()
    app.exec_()
