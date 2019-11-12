import shutil
import subprocess
import os
import fserror
import os.path
import send2trash


class FileSystemCommander:
    def delete(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    def copy(self, path, dst):
        if os.path.isdir(path):
            try:
                subprocess.run(['cp', '-r', path, dst])
            except subprocess.CalledProcessError:
                raise fserror.CopyFileError
        else:
            shutil.copy2(path, dst, follow_symlinks=False)

    def move(self, path, dst):
        shutil.move(path, dst)

    def moveToTrash(self, path):
        send2trash.send2trash(path)

    def openFile(self, path):
        try:
            subprocess.run(['xdg-open', path], check=True)
        except subprocess.CalledProcessError:
            raise fserror.OpenFileError

    def rename(self, path, newName):
        pathTree = path.split('/')
        pathTree[-1] = newName
        newPath = '/'.join(pathTree)
        shutil.move(path, newPath)