import ctypes

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QImage, QFont, QIcon
from PyQt5.QtWidgets import QMainWindow

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
        style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
        font = QFont('Century Gothic', 18)
        font.setBold(True)
        self.labelLinkDaniil = QtWidgets.QLabel(Dialog)
        self.labelLinkDaniil.setFont(font)
        self.labelLinkDaniil.setGeometry(QtCore.QRect(330, 20, 350, 100))
        self.labelLinkDaniil.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLinkDaniil.setObjectName("labelLinkDaniil")
        self.labelLinkDaniil.setText('Зайцев Д.В <a href="https://vk.com/shhiz0id">ВКонтакте</a>')
        self.labelLinkDaniil.setOpenExternalLinks(True)
        self.labelLinkAlbert = QtWidgets.QLabel(Dialog)
        self.labelLinkAlbert.setFont(font)
        self.labelLinkAlbert.setGeometry(QtCore.QRect(330, 40, 400, 100))
        self.labelLinkAlbert.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLinkAlbert.setObjectName("labelLinkAlbert")
        self.labelLinkAlbert.setText('Николаев А.П. <a href="https://vk.com/namsen">ВКонтакте</a>')
        self.labelLinkAlbert.setOpenExternalLinks(True)
        self.labelLinkAnton = QtWidgets.QLabel(Dialog)
        self.labelLinkAnton.setFont(font)
        self.labelLinkAnton.setGeometry(QtCore.QRect(330, 20, 450, 100))
        self.labelLinkAnton.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLinkAnton.setObjectName("labelLinkAnton")
        self.labelLinkAnton.setText('Смирнов А.А <a href="https://vk.com/anothertrash">ВКонтакте</a>')
        self.labelLinkAnton.setOpenExternalLinks(True)
        self.ButtonBack = QtWidgets.QPushButton(Dialog)
        self.ButtonBack.setGeometry(QtCore.QRect(300, 260, 340, 80))
        self.ButtonBack.setObjectName("ButtonStart")
        self.ButtonBack.setStyleSheet(style)
        self.ButtonBack.setFont(QFont('Century Gothic', 13))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ButtonBack.setText(_translate("Dialog", "Назад"))


class Authors(QMainWindow, Ui_Dialog):
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
        self.setWindowTitle('Авторы')
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

        self.labelLinkDaniil.move(int((self.width() / 2) - (self.labelLinkDaniil.width() / 2)),
                                  int(self.height() * 0.2898550724637681))

        self.labelLinkAlbert.move(int((self.width() / 2) - (self.labelLinkAlbert.width() / 2)),
                                  int(self.labelLinkDaniil.y() + self.height() * 0.072463768115942))

        self.labelLinkAnton.move(int((self.width() / 2) - (self.labelLinkAnton.width() / 2)),
                                  int(self.labelLinkAlbert.y() + self.height() * 0.072463768115942))

        self.ButtonBack.setFixedSize(int(self.width() * 0.4297), int(self.height() * 0.104))
        self.ButtonBack.move(int((self.width() / 2) - (self.ButtonBack.width() / 2)), int(self.height() * 0.802))

        return super(Authors, self).resizeEvent(event)

    def logic(self):
        self.ButtonBack.clicked.connect(self.back)

    def back(self):
        self.close()
        from Main import Main
        self.w = Main(self.topic, self.width(), self.height(), self.isMaximized())
        self.w.show()

    def design(self):
        if self.topic == "white":
            style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
            self.ButtonBack.setStyleSheet(style)
        else:
            style = 'background: rgb(10,10,10);color: rgb(255,255,255); \
                                             border-color: rgb(255,255,255);border-style: solid; \
                                             border-radius: 4px; border-width: 3px;'
            self.ButtonBack.setStyleSheet(style)
            style = 'color: rgb(255,255,255);'
            self.labelLinkDaniil.setStyleSheet(style)
            self.labelLinkAlbert.setStyleSheet(style)
            self.labelLinkAnton.setStyleSheet(style)
