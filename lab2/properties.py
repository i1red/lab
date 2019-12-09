from PyQt5.QtWidgets import QDialog
from ui import Ui_PropertiesDialog
from filestats import FileStats


class PropertiesDialog(QDialog):
    def __init__(self, path):
        super().__init__()
        self._ui = Ui_PropertiesDialog()
        self._ui.setupUi(self)

        self._filestats = FileStats(path)
        self._ui.lineEditName.setText(self._filestats.name)
        self._setUpComboBoxes()
        self._selUpLabels()

        self._ui.buttonSave.clicked.connect(self._save_clicked)


    def _setUpComboBoxes(self):
        perms = self._filestats.permissions
        PropertiesDialog._setComboBox(self._ui.comboBoxOwner, perms[:2])
        PropertiesDialog._setComboBox(self._ui.comboBoxGroup, perms[3:5])
        PropertiesDialog._setComboBox(self._ui.comboBoxOthers, perms[6:8])

    def _selUpLabels(self):
        self._ui.labelSizeValue.setText(str(self._filestats.fileSize()))
        self._ui.labelAccessedValue.setText(self._filestats.lastAccessed())
        self._ui.labelModifiedValue.setText(self._filestats.lastModified())


    def _save_clicked(self):
        permsMap = {0: '--', 1: 'r-', 2: 'rw'}

        self._filestats.setPermissions(permsMap[self._ui.comboBoxOwner.currentIndex()],
                                       permsMap[self._ui.comboBoxGroup.currentIndex()],
                                       permsMap[self._ui.comboBoxOthers.currentIndex()])

        self._filestats.name = self._ui.lineEditName.text()


    @staticmethod
    def _setComboBox(comboBox, permissions):
        index = 0

        if permissions[0] == 'r':
            index = 2 if permissions[1] == 'w' else 1

        comboBox.setCurrentIndex(index)
