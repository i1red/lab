from PyQt5.QtWidgets import QMainWindow, QFileSystemModel, QInputDialog
from PyQt5.QtWidgets import QMessageBox
from ui import Ui_MainWindow
from fileerror import *
from properties import PropertiesDialog
import filecommands


def throwError(text):
    message = QMessageBox(QMessageBox.Critical, 'ERROR!', text)
    message.exec()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._model = QFileSystemModel()
        self._model.setRootPath('/')

        self._setUpViews(self._ui.leftView)
        self._setUpViews(self._ui.rightView)

        self._setUpActions()

        self._setUpButtons()

    def _setUpViews(self, view):
        view.setModel(self._model)
        view.setRootIndex(self._model.index(self._model.rootPath()))
        view.doubleClicked.connect(self._view_doubleClicked)

    def _setUpActions(self):
        self._ui.actionNewFile.triggered.connect(self._newFile_triggered)
        self._ui.actionNewFolder.triggered.connect(self._newFolder_triggered)
        self._ui.actionRename.triggered.connect(self._properties_triggered)
        self._ui.actionMove.triggered.connect(self._move_triggered)
        self._ui.actionCopy.triggered.connect(self._copy_triggered)
        self._ui.actionToTrash.triggered.connect(self._toTrash_triggered)
        self._ui.actionDelete.triggered.connect(self._delete_triggered)

    def _setUpButtons(self):
        self._ui.leftBackButton.clicked.connect(self._leftBack_clicked)
        self._ui.rightBackButton.clicked.connect(self._rightBack_clicked)
        self._ui.leftHomeButton.clicked.connect(self._leftHome_clicked)
        self._ui.rightHomeButton.clicked.connect(self._rightHome_clicked)

    def _newFile_triggered(self):
        print('newFile')
        path = self._getCurrentLocation()
        newFile, confirmed = QInputDialog.getText(self, 'Create new file', 'File name: ')

        if confirmed:
            try:
                filecommands.newFile(path + '/' + newFile)
            except CreateFileError:
                throwError(f'Can NOT create file {newFile}')

    def _newFolder_triggered(self):
        print('newFolder')
        path = self._getCurrentLocation()
        newFolder, confirmed = QInputDialog.getText(self, 'Create new folder', 'Folder name: ')

        if confirmed:
            try:
                filecommands.newFolder(path + '/' + newFolder)
            except CreateFolderError:
                throwError(f'Can NOT create folder {newFolder}')

    def _properties_triggered(self):
        print('properties')
        paths = self._getSelectedItemsPath()

        for path in paths:
            dialog = PropertiesDialog(path)
            dialog.exec_()

    def _move_triggered(self):
        print('move')
        paths = self._getSelectedItemsPath()
        dst = self._getDestination()

        for path in paths:
            try:
                filecommands.move(path, dst)
            except MoveFileError:
                throwError(f'Can NOT move {path} to {dst}')

    def _copy_triggered(self):
        print('copy')
        paths = self._getSelectedItemsPath()
        dst = self._getDestination()

        for path in paths:
            try:
                filecommands.copy(path, dst)
            except CopyFileError:
                throwError(f'Can NOT copy {path} to {dst}')

    def _toTrash_triggered(self):
        print('toTrash')
        paths = self._getSelectedItemsPath()

        for path in paths:
            try:
                filecommands.moveToTrash(path)
            except MoveToTrashError:
                throwError(f'Can NOT move {path} to trash')

    def _delete_triggered(self):
        print('delete')
        paths = self._getSelectedItemsPath()

        for path in paths:
            try:
                filecommands.delete(path)
            except DeleteFileError:
                throwError(f'Can NOT delete {path}')

    def _leftBack_clicked(self):
        self._goBack(self._ui.leftView)

    def _rightBack_clicked(self):
        self._goBack(self._ui.rightView)

    def _leftHome_clicked(self):
        self._goHome(self._ui.leftView)

    def _rightHome_clicked(self):
        self._goHome(self._ui.rightView)

    def _view_doubleClicked(self, index):
        view = self.sender()
        firstColumnIndex = index.siblingAtColumn(0)
        fileInfo = self._model.fileInfo(firstColumnIndex)

        if fileInfo.isDir():
            if fileInfo.isReadable():
                view.setRootIndex(firstColumnIndex)
            else:
                message = QMessageBox(QMessageBox.Critical, 'Permission denied',
                                      f'Folder {fileInfo.fileName()} is not readable!')
                message.exec()
        elif fileInfo.isFile():
            try:
                filecommands.openFile(fileInfo.absoluteFilePath())
            except OpenFileError:
                message = QMessageBox(QMessageBox.Critical, 'Can NOT open file', f'Can not open {fileInfo.fileName()}')
                message.exec()

    def _goBack(self, view):
        index = view.rootIndex()
        if index != self._model.index(filecommands.ROOT_PATH):
            view.setRootIndex(index.parent())

    def _goHome(self, view):
        view.setRootIndex(self._model.index(filecommands.ROOT_PATH))

    def _getSelectedItemsPath(self):
        return {self._model.fileInfo(index).absoluteFilePath() for index in self._ui.leftView.selectedIndexes()}

    def _getCurrentLocation(self):
        return self._model.fileInfo(self._ui.leftView.rootIndex()).absoluteFilePath()

    def _getDestination(self):
        return self._model.fileInfo(self._ui.rightView.rootIndex()).absoluteFilePath()
