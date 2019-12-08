import shutil
import subprocess
import os
import fserror
import os.path
import send2trash


class FileSystemCommander:
    @staticmethod
    def rootPath():
        return '/'

    @staticmethod
    def newFile(path):
        try:
            f = open(path, 'w+')
            f.close()
        except Exception:
            raise fserror.CreateFileError

    @staticmethod
    def newFolder(path):
        try:
            os.mkdir(path)
        except Exception:
            raise fserror.CreateFolderError

    @staticmethod
    def delete(path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except Exception:
            raise fserror.DeleteFileError

    @staticmethod
    def copy(path, dst):
        try:
            if os.path.isdir(path):
                subprocess.run(['cp', '-r', path, dst])
            else:
                shutil.copy2(path, dst, follow_symlinks=False)
        except Exception:
            raise fserror.CopyFileError

    @staticmethod
    def move(path, dst):
        try:
            shutil.move(path, dst)
        except Exception:
            raise fserror.MoveFileError

    @staticmethod
    def moveToTrash(path):
        try:
            send2trash.send2trash(path)
        except Exception:
            raise fserror.MoveToTrashError

    @staticmethod
    def openFile(path):
        try:
            subprocess.run(['xdg-open', path], check=True)
        except subprocess.CalledProcessError:
            raise fserror.OpenFileError

    @staticmethod
    def rename(path, newName):
        pathTree = path.split('/')
        pathTree[-1] = newName
        newPath = '/'.join(pathTree)
        try:
            shutil.move(path, newPath)
        except Exception:
            raise fserror.RenameFileError