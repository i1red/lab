from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtCore import QDir
from fscommander import FileSystemCommander


class FileSysModel(QFileSystemModel):
    def __init__(self, parent):
        super().__init__(parent)

        self.setReadOnly(False)
        self.setFilter(QDir.AllEntries)
        self.setRootPath(FileSystemCommander.rootPath())