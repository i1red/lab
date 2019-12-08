from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize, QCoreApplication
from main_widget import MainWidget


class MainWindow(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.toolbar = self.addToolBar('Actions')

        self.setupUI()
        self.retranslateUI(title)

    def setupUI(self):
        self.resize(1280, 720)
        self.setMinimumSize(QSize(1280, 720))
        self.setCentralWidget(MainWidget(self))

    def retranslateUI(self, title):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate(title, title))