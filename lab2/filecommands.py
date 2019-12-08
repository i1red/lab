import shutil
import subprocess
import os
import os.path
import send2trash
from fileerror import *


ROOT_PATH = '/'


def newFile(path):
    try:
        f = open(path, 'w+')
        f.close()
    except Exception:
        raise CreateFileError


def newFolder(path):
    try:
        os.mkdir(path)
    except Exception:
        raise CreateFolderError


def delete(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except Exception:
        raise DeleteFileError


def copy(path, dst):
    try:
        if os.path.isdir(path):
            subprocess.run(['cp', '-r', path, dst])
        else:
            shutil.copy2(path, dst, follow_symlinks=False)
    except Exception:
        raise CopyFileError


def move(path, dst):
    try:
        shutil.move(path, dst)
    except Exception:
        raise MoveFileError


def moveToTrash(path):
    try:
        send2trash.send2trash(path)
    except Exception:
        raise MoveToTrashError


def openFile(path):
    try:
        subprocess.run(['xdg-open', path], check=True)
    except subprocess.CalledProcessError:
        raise OpenFileError


def rename(path, newName):
    pathTree = path.split('/')
    pathTree[-1] = newName
    newPath = '/'.join(pathTree)
    try:
        shutil.move(path, newPath)
    except Exception:
        raise RenameFileError
