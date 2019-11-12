import sys
from PyQt5.QtWidgets import QApplication
from resources.main_window import MainWindow


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.mainWindow = MainWindow('Linux File Manager')

    def run(self):
        self.mainWindow.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    app = App()
    app.run()