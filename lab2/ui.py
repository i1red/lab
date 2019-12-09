from PyQt5 import uic


MAIN_WINDOW_UI_FILE = 'mainwindow.ui'
Ui_MainWindow, _ = uic.loadUiType(MAIN_WINDOW_UI_FILE)


PROPERTIES_DIALOG_UI_FILE = 'properties.ui'
Ui_PropertiesDialog, _ = uic.loadUiType(PROPERTIES_DIALOG_UI_FILE)
