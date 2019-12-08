from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMessageBox, QInputDialog, QTableView
from PyQt5.QtGui import QIcon
from non_expandable_tree_view import NonExpandableTree
from file_system_model import FileSysModel
from menu_action import MenuAction
from fscommander import FileSystemCommander
import fserror



class MainWidget(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.model = FileSysModel(self)
        self.leftTree = NonExpandableTree(self, self.layout, self.model, doubleClicked=self.tree_doubleClicked)
        self.rightTree = NonExpandableTree(self, self.layout, self.model, doubleClicked=self.tree_doubleClicked)

        actions = [MenuAction(QIcon(), 'New file', mainWindow, clicked=self.newFile_clicked),
                   MenuAction(QIcon(), 'New folder', mainWindow, clicked=self.newFolder_clicked),
                   MenuAction(QIcon(), 'Rename', mainWindow, clicked=self.rename_clicked),
                   MenuAction(QIcon(), 'Move', mainWindow, clicked=self.move_clicked),
                   MenuAction(QIcon(), 'Copy', mainWindow, clicked=self.copy_clicked),
                   MenuAction(QIcon(), 'To trash', mainWindow, clicked=self.toTrash_clicked),
                   MenuAction(QIcon(), 'Delete', mainWindow, clicked=self.delete_clicked)]

        for action in actions:
            mainWindow.toolbar.addAction(action)

    def getSelectedItemsPath(self):
        return [self.model.fileInfo(index).absoluteFilePath() for index in self.leftTree.selectedIndexes()]

    def getCurrentLocation(self):
        return self.model.fileInfo(self.leftTree.rootIndex()).absoluteFilePath()

    def getDestination(self):
        return self.model.fileInfo(self.rightTree.rootIndex()).absoluteFilePath()

    @staticmethod
    def trhowError(text):
        message = QMessageBox(QMessageBox.Critical, 'ERROR!', text)
        message.exec()

    def newFile_clicked(self):
        path = self.getCurrentLocation()
        newFile, confirmed = QInputDialog.getText(self, 'Create new file', 'File name: ')
        if confirmed:
            try:
                FileSystemCommander.newFile(path + '/' + newFile)
            except fserror.CreateFileError:
                MainWidget.trhowError(f'Can NOT create file {newFile}')

    def newFolder_clicked(self):
        path = self.getCurrentLocation()
        newFolder, confirmed = QInputDialog.getText(self, 'Create new folder', 'Folder name: ')
        if confirmed:
            try:
                FileSystemCommander.newFolder(path + '/' + newFolder)
            except fserror.CreateFolderError:
                MainWidget.trhowError(f'Can NOT create folder {newFolder}')

    def rename_clicked(self):
        paths = self.getSelectedItemsPath()
        for path in paths:
            pathTree = path.split('/')
            name = pathTree[-1]
            newName, confirmed = QInputDialog.getText(self, 'Rename file/folder', f'Rename {name} to:')
            if confirmed:
                try:
                    FileSystemCommander.rename(path, newName)
                except fserror.RenameFileError:
                    MainWidget.trhowError(f'Can NOT rename {name} to {newName}')

    def move_clicked(self):
        paths = self.getSelectedItemsPath()
        dst = self.getDestination()
        for path in paths:
            try:
                FileSystemCommander.move(path, dst)
            except fserror.MoveFileError:
                MainWidget.trhowError(f'Can NOT move {path} to {dst}')

    def copy_clicked(self):
        paths = self.getSelectedItemsPath()
        dst = self.getDestination()
        for path in paths:
            try:
                FileSystemCommander.copy(path, dst)
            except fserror.CopyFileError:
                MainWidget.trhowError(f'Can NOT copy {path} to {dst}')

    def toTrash_clicked(self):
        paths = self.getSelectedItemsPath()
        for path in paths:
            try:
                FileSystemCommander.moveToTrash(path)
            except fserror.MoveToTrashError:
                MainWidget.trhowError(f'Can NOT move {path} to trash')

    def delete_clicked(self):
        paths = self.getSelectedItemsPath()
        for path in paths:
            try:
                FileSystemCommander.delete(path)
            except fserror.DeleteFileError:
                MainWidget.trhowError(f'Can NOT delete {path}')


    def tree_doubleClicked(self, index):
        tree = self.sender()
        fileInfo = self.model.fileInfo(index)

        if fileInfo.fileName() == '..':
            directory = fileInfo.dir()
            directory.cdUp()
            tree.setRootIndex(self.model.index(directory.absolutePath()))
        elif fileInfo.fileName() == '.':
            tree.setRootIndex(self.model.index('/'))
        elif fileInfo.isDir():
            if fileInfo.isReadable():
                tree.setRootIndex(index)
            else:
                message = QMessageBox(QMessageBox.Critical, 'Permission denied',
                                      f'Folder {fileInfo.fileName()} is not readable!')
                message.exec()
        elif fileInfo.isFile():
            try:
                FileSystemCommander.openFile(fileInfo.absoluteFilePath())
            except fserror.OpenFileError:
                message = QMessageBox(QMessageBox.Critical, 'Can NOT open file', f'Can not open {fileInfo.fileName()}')
                message.exec()