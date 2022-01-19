import ctypes
import glob
import sys
from typing import List

from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont, QImage, QIcon
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QLabel, QFileDialog, QDialog, QDialogButtonBox, \
    QFormLayout, QLineEdit

from Courses import Courses
from ITcube import ITcube
from Participant import Participant

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
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 1240, 610))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        delegate = ReadOnlyDelegate(self.tableWidget)
        self.tableWidget.setItemDelegateForColumn(0, delegate)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setFont(QFont('Century Gothic', 10))
        self.pushButtonDoS = QtWidgets.QPushButton(Dialog)
        self.pushButtonDoS.setGeometry(QtCore.QRect(170, 650, 300, 50))
        self.pushButtonDoS.setObjectName("pushButtonDoS")
        self.pushButtonDoS.setFont(QFont('Century Gothic', 8))
        self.pushButtonImport = QtWidgets.QPushButton(Dialog)
        self.pushButtonImport.setGeometry(QtCore.QRect(790, 650, 300, 50))
        self.pushButtonImport.setObjectName("pushButtonImport")
        self.pushButtonImport.setFont(QFont('Century Gothic', 8))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButtonImport.setText(_translate("Dialog", "Импортировать данные из файла"))
        self.pushButtonDoS.setText(_translate("Dialog", "Ввести данные вручную"))


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


class App(QMainWindow):
    def __init__(self):
        super().__init__()

    def load_image(self, photo, mak):
        self.photo = photo
        self.n = mak.split()[1]
        self.setWindowTitle(f"Макет {self.n}")
        pixmap = QPixmap(self.photo[int(self.n) - 1])
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())
        self.setFixedSize(pixmap.width(), pixmap.height())


class Pattern(QMainWindow, Ui_Dialog):
    resized = QtCore.pyqtSignal()

    def __init__(self, topic, x, y, m):
        super().__init__()
        self.topic = topic
        self.maket = "Макет 1"
        if topic == "white":
            self.im = QImage()
            self.im.load("images/white_background.jpg")
        else:
            self.im = QImage()
            self.im.load("images/black_background.jpg")
        self.setupUi(self, topic)
        self.design()
        self.setWindowTitle('Выбор макетов')
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

    def resizeEvent(self, event):
        self.resized.emit()
        self.resize_image()

        self.tableWidget.setFixedSize(int(self.width() * 0.975), int(self.height() * 0.84722))

        self.pushButtonDoS.move(int(self.width() * 0.1328125), int(self.height() * 0.90277))
        self.pushButtonDoS.setFixedSize(int(self.width() * 0.234375), int(self.height() * 0.06944))

        self.pushButtonImport.move(int(self.width() * 0.6171875), int(self.height() * 0.902777))
        self.pushButtonImport.setFixedSize(int(self.width() * 0.234375), int(self.height() * 0.06944))

        return super(Pattern, self).resizeEvent(event)

    def logic(self):
        self.photos = glob.glob("certificates/*")
        self.tableWidget.setRowCount(len(self.photos))
        for col, i in enumerate(self.photos):
            btn = Qt.QPushButton(f"Макет {col + 1}")
            btn.clicked.connect(self.show_photo)
            self.tableWidget.setCellWidget(col, 0, btn)

        self.pushButtonImport.clicked.connect(self.file)
        self.pushButtonDoS.clicked.connect(self.vruch)

    def show_photo(self):
        name = self.sender().text()
        self.maket = name
        self.ex = App()
        self.ex.load_image(self.photos, name)
        self.ex.show()

    def vruch(self):
        if self.maket == "Макет 2":
            dialog = InputDialog(labels=["Степень Диплома", "Тип Диплома", "Название Конкурса", "Название Номинации",
                                         "Имя Научного Руководителя"])
            if not dialog.exec():
                return
            rez = dialog.getInputs()
            self.w = ITcube(*rez)
            sys.exit()
        elif self.maket == "Макет 3":
            dialog = InputDialog(labels=["Имя", "Дата"])
            if not dialog.exec():
                return
            rez = dialog.getInputs()
            self.w = Participant(*rez)
            sys.exit()
        elif self.maket == "Макет 1":
            dialog = InputDialog(labels=["Имя", "Название Курса", "Дата"])
            if not dialog.exec():
                return
            rez = dialog.getInputs()
            self.w = Courses(*rez)
            sys.exit()

    def file(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', "Книга Excel (*.xlsx)")[0]

    def design(self):
        if self.topic == "white":
            style = 'background: rgb(255,255,255);color: rgb(0,0,0);'
            self.pushButtonImport.setStyleSheet(style)
            self.pushButtonDoS.setStyleSheet(style)
            self.tableWidget.setStyleSheet(style)
        else:
            style = 'background: rgb(10,10,10);color: rgb(255,255,255); \
                     border-color: rgb(255,255,255);border-style: solid; \
                     border-radius: 4px; border-width: 3px;'
            self.pushButtonImport.setStyleSheet(style)
            self.pushButtonDoS.setStyleSheet(style)
            self.tableWidget.setStyleSheet(style)


class InputDialog(QDialog):
    def __init__(self, labels: List[str], parent=None):
        super().__init__(parent)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        layout = QFormLayout(self)

        self.inputs = []
        for lab in labels:
            self.inputs.append(QLineEdit(self))
            layout.addRow(lab, self.inputs[-1])

        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return tuple(input.text() for input in self.inputs)
