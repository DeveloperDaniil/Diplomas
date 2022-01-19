import ctypes
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QImage, QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication

from Authors import Authors
from Pattern import Pattern

myAppId = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class Ui_Dialog(object):
    def setupUi(self, Dialog, topic):
        Dialog.setObjectName("Dialog")
        Dialog.setMinimumSize(1024, 768)
        if topic == "white":
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(QPixmap("images/white_background.jpg")))
            Dialog.setPalette(palette)
        else:
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(QPixmap("images/black_background.jpg")))
            Dialog.setPalette(palette)
        self.ButtonReColour = QtWidgets.QPushButton(Dialog)
        self.ButtonReColour.setGeometry(QtCore.QRect(0, 0, 31, 28))
        self.ButtonReColour.setText("")
        if topic == "white":
            self.ButtonReColour.setIcon(QtGui.QIcon('images/re_colour_white.png'))
        else:
            self.ButtonReColour.setIcon(QtGui.QIcon('images/re_colour_black.png'))
        self.ButtonReColour.setObjectName("ButtonReColour")
        self.ButtonReColour.setStyleSheet('background: rgba(255,255,255,0);')
        self.ButtonStart = QtWidgets.QPushButton(Dialog)
        self.ButtonStart.setGeometry(QtCore.QRect(300, 260, 551, 71))
        self.ButtonStart.setObjectName("ButtonStart")
        self.ButtonStart.setFont(QFont('Century Gothic', 13))
        self.ButtonAftors = QtWidgets.QPushButton(Dialog)
        self.ButtonAftors.setGeometry(QtCore.QRect(300, 340, 551, 71))
        self.ButtonAftors.setObjectName("ButtonAftors")
        self.ButtonAftors.setFont(QFont('Century Gothic', 13))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ButtonStart.setText(_translate("Dialog", "Выбрать макет"))
        self.ButtonAftors.setText(_translate("Dialog", "Авторы"))


class Main(QMainWindow, Ui_Dialog):
    resized = QtCore.pyqtSignal()

    def __init__(self, topic="white", x=1024, y=768, m=False):
        super().__init__()
        self.topic = topic
        if topic == "white":
            self.im = QImage()
            self.im.load("images/white_background.jpg")
        else:
            self.im = QImage()
            self.im.load("images/black_background.jpg")
        self.setupUi(self, topic)
        self.setWindowTitle('Мастерская Дипломов')
        self.design()
        if m:
            self.showMaximized()
        else:
            self.resize(x, y)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.logic()

    def resize_image(self):
        if (self.width() > 2560) or (self.height() > 1440):
            size = (self.width(), self.height())
            imR = self.im.scaled(size[0], size[1])
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(QPixmap(QPixmap.fromImage(imR))))
            self.setPalette(palette)
            return
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(QPixmap.fromImage(self.im))))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.resized.emit()
        self.resize_image()

        self.ButtonStart.move(int(self.width() * 0.286), int(self.height() * 0.42))
        self.ButtonStart.setFixedSize(int(self.width() * 0.4276), int(self.height() * 0.095))

        self.ButtonAftors.move(int(self.width() * 0.286), int(self.height() * 0.53))
        self.ButtonAftors.setFixedSize(int(self.width() * 0.4276), int(self.height() * 0.095))

        return super(Main, self).resizeEvent(event)

    def logic(self):
        self.ButtonReColour.clicked.connect(self.re_color)
        self.ButtonStart.clicked.connect(self.new_win)
        self.ButtonAftors.clicked.connect(self.aftors)

    def aftors(self):
        self.close()
        self.w = Authors(self.topic, self.width(), self.height(), self.isMaximized())
        self.w.show()

    def new_win(self):
        self.close()
        self.w = Pattern(self.topic, self.width(), self.height(), self.isMaximized())
        self.w.show()

    def re_color(self):
        if self.topic == "white":
            self.topic = "black"
            self.im.load("images/black_background.jpg")
            style = 'background: rgb(10,10,10);color: rgb(255,255,255);border-style: solid; \
                            border-radius: 4px; border-width: 3px;'
            self.ButtonReColour.setIcon(QtGui.QIcon('images/re_colour_black.png'))
        else:
            self.topic = "white"
            self.im.load("images/white_background.jpg")
            style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
            self.ButtonReColour.setIcon(QtGui.QIcon('images/re_colour_white.png'))
        self.ButtonStart.setStyleSheet(style)
        self.ButtonAftors.setStyleSheet(style)
        self.resize_image()

    def design(self):
        if self.topic == "white":
            style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
            self.ButtonStart.setStyleSheet(style)
            self.ButtonAftors.setStyleSheet(style)
        else:
            style = 'background: rgb(10,10,10);color: rgb(255,255,255); \
                                 border-color: rgb(255,255,255);border-style: solid; \
                                 border-radius: 4px; border-width: 3px;'
            self.ButtonStart.setStyleSheet(style)
            self.ButtonAftors.setStyleSheet(style)


try:
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = Main()
        ex.show()
        sys.exit(app.exec())
except Exception as e:
    print(e.__class__.__name__)
