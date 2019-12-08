from PyQt5.QtWidgets import QAction


class MenuAction(QAction):
    def __init__(self, *args, clicked):
        super().__init__(*args)

        self.triggered.connect(clicked)