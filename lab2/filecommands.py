import shutil
import subprocess
import os
import os.path
import send2trash
from fileerror import *


ROOT_PATH = '/'



def uniquePath(path):
    tmp = path.split('/')
    dir = '/'.join(tmp[:-1]) + '/'
    name, ext = os.path.splitext(tmp[-1])
    nameWithExt = lambda x: f'{name}({x}){ext}'
    res = dir + nameWithExt(1)

    i = 2
    while os.path.exists(res):
        res = dir + nameWithExt(i)
        i += 1

    return res


def delete(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except Exception:
        raise DeleteFileError


def chosenOption(path, changeIfExists):
    option = changeIfExists(path)
    if option == 2:
        return uniquePath(path)
    if option == 1:
        delete(path)
        return path
    if option == 0:
        return None


def newItem(func):
    def wrap(path, changeIfExists):
        if os.path.exists(path):
            path = chosenOption(path, changeIfExists)

        return func(path) if path is not None else None

    return wrap


def fullDst(func):
    def wrap(path, dst, changeIfExists):
        fullDst = dst + '/' + path.split('/')[-1]
        return func(path, fullDst, changeIfExists)

    return wrap


def copyMoveRename(func):
    def wrap(path, dst, changeIfExists):
        if os.path.exists(dst):
            dst = chosenOption(dst, changeIfExists)

        return func(path, dst) if dst is not None else None

    return wrap


@newItem
def newFile(path):
    try:
        f = open(path, 'w+')
        f.close()
    except Exception:
        raise CreateFileError


@newItem
def newFolder(path):
    try:
        os.mkdir(path)
    except Exception:
        raise CreateFolderError

@fullDst
@copyMoveRename
def copy(path, dst):
    try:
        if os.path.isdir(path):
            subprocess.run(['cp', '-r', path, dst])
        else:
            shutil.copy2(path, dst, follow_symlinks=False)
    except Exception:
        raise CopyFileError


@fullDst
@copyMoveRename
def move(path, dst):
    try:
        shutil.move(path, dst)
    except Exception:
        raise MoveFileError


@copyMoveRename
def rename(oldPath, newPath):
    try:
        shutil.move(oldPath, newPath)
    except Exception:
        raise RenameFileError


def moveToTrash(path):
    try:
        send2trash.send2trash(path)
    except Exception:
        raise MoveToTrashError


def openWithDefaultApp(path):
    try:
        subprocess.run(['xdg-open', path], check=True)
    except subprocess.CalledProcessError:
        raise OpenFileError


