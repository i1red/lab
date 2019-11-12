import sys
import shutil
import getpass
import subprocess
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileSystemModel, QMessageBox, QMenu, QPushButton, QAction, QLineEdit, QInputDialog
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtCore import QDir, QUrl
from fscommander import FileSystemCommander
import fserror



class MainWidget(QtWidgets.QWidget):
    def __init__(self, window, commander):
        super().__init__()

        self.layout = QtWidgets.QHBoxLayout(self)


        self.treeView = self.addTreeView()
        self.ltList = self._addListView()
        self.rtList = self._addListView()

        self.model = self._setupFileSystemModel()


        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index('/'))
        self.ltList.setModel(self.model)
        self.ltList.setRootIndex(self.model.index('/'))
        self.rtList.setModel(self.model)
        self.rtList.setRootIndex(self.model.index('/'))


        self.ltList.doubleClicked.connect(self.listViewDoubleClicked)
        self.rtList.doubleClicked.connect(self.listViewDoubleClicked)

        #self.ltList.contextMenuEvent = self.listViewRbClicked

        self.commander = commander

        actionNew = QAction(QIcon(), 'new', window)
        actionNew.triggered.connect(self.newClicked)

        actionMove = QAction(QIcon(), 'move', window)
        actionMove.triggered.connect(self.moveClicked)

        actionMoveToTrash = QAction(QIcon(), 'move to trash', window)
        actionMoveToTrash.triggered.connect(self.moveToTrashClicked)

        actionCopy = QAction(QIcon(), 'copy', window)
        actionCopy.triggered.connect(self.copyClicked)

        actionDelete = QAction(QIcon(), 'delete', window)
        actionDelete.triggered.connect(self.deleteClicked)

        actionRename = QAction(QIcon(), 'rename', window)
        actionRename.triggered.connect(self.renameClicked)

        tbActions = [actionNew, actionMove, actionDelete, actionMoveToTrash, actionCopy, actionRename]

        for action in tbActions:
            window.toolbar.addAction(action)

    def addTreeView(self):
        treeView = QtWidgets.QTreeView(self)
        treeView.setEnabled(True)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        treeView.setSizePolicy(sizePolicy)
        self.layout.addWidget(treeView)

        return treeView

    def _addListView(self):
        listView = QtWidgets.QListView(self)
        listView.setEnabled(True)

        listSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        listSizePolicy.setHorizontalStretch(0)
        listSizePolicy.setVerticalStretch(0)

        listView.setSizePolicy(listSizePolicy)
        self.layout.addWidget(listView)

        return listView

    def getSelectedItemsPath(self):
        return [self.model.fileInfo(index).absoluteFilePath() for index in self.ltList.selectedIndexes()]

    def getDestination(self):
        return self.model.fileInfo(self.rtList.rootIndex()).absoluteFilePath()

    def newClicked(self):
        print('kek')

    def copyClicked(self):
        paths = self.getSelectedItemsPath()
        dst = self.getDestination()
        for path in paths:
            self.commander.copy(path, dst)

    def moveToTrashClicked(self):
        paths = self.getSelectedItemsPath()
        for path in paths:
            self.commander.moveToTrash(path)

    def moveClicked(self):
        paths = self.getSelectedItemsPath()
        dst = self.getDestination()
        for path in paths:
            self.commander.move(path, dst)

    def deleteClicked(self):
        paths = self.getSelectedItemsPath()
        for path in paths:
            self.commander.delete(path)

    def renameClicked(self):
        paths = self.getSelectedItemsPath()
        for path in paths:
            pathTree = path.split('/')
            name = pathTree[-1]
            newName, ok = QInputDialog.getText(self, 'Rename file/folder', f'Rename {name} to:')
            if ok:
                self.commander.rename(path, newName)


    def _setupFileSystemModel(self):
        fileSysModel = QFileSystemModel(self)
        fileSysModel.setReadOnly(False)
        fileSysModel.setFilter(QDir.AllEntries)
        fileSysModel.setRootPath('/')

        return fileSysModel

    def listViewDoubleClicked(self, index):
        listView = self.sender()
        fileInfo = self.model.fileInfo(index)

        if fileInfo.fileName() == '..':
            directory = fileInfo.dir()
            directory.cdUp()
            listView.setRootIndex(self.model.index(directory.absolutePath()))
        elif fileInfo.fileName() == '.':
            listView.setRootIndex(self.model.index('/'))
        elif fileInfo.isDir():
            if fileInfo.isReadable():
                listView.setRootIndex(index)
            else:
                message = QMessageBox()
                message.setIcon(QMessageBox.Critical)
                message.setWindowTitle('Permission denied')
                message.setText(f'Folder {fileInfo.fileName()} is not readable!')
                message.exec()
        elif fileInfo.isFile():
            try:
                self.commander.openFile(fileInfo.absoluteFilePath())
            except fserror.OpenFileError:
                message = QMessageBox()
                message.setIcon(QMessageBox.Critical)
                message.setWindowTitle("Can't open file")
                message.setText(f"Can't open {fileInfo.fileName()}")
                message.exec()


class UIMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.toolbar = self.addToolBar('kek')
        self._setupUI()
        self._retranslateUI()

    def _setupUI(self):
        #self.setObjectName('UIMainWindow')shell=True,
        self.resize(800, 600)
        self.setMinimumSize(QtCore.QSize(800, 600))
        self.setCentralWidget(MainWidget(self, FileSystemCommander()))

    def _retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('Linux File Manager', 'Linux File Manager'))


class App:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.mainWindow = UIMainWindow()

    def run(self):
        self.mainWindow.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    app = App()
    app.run()