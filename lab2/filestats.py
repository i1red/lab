import os
import grp
import pwd
import time
import stat
import subprocess
from filecommands import rename


class FileStats:
    def __init__(self, path):
        fstats = os.stat(path)
        permissions = stat.filemode(fstats.st_mode)
        splitPath = path.split('/')

        self._name = splitPath[-1]
        splitPath.pop()
        self._dir = '/' + '/'.join(splitPath) + ('/' if len(splitPath) > 0 else '')

        self._isDir = permissions[0] == 'd'
        self._permissionsOwner = tuple(permissions[1:3])
        self._permissionsGroup = tuple(permissions[4:6])
        self._permissionsOthers = tuple(permissions[7:9])

        self._ownerName = pwd.getpwuid(fstats.st_uid).pw_name
        self._groupName = grp.getgrgid(fstats.st_gid).gr_name

        self._fileSize = FileStats._convertFileSize(FileStats._dirSize(path))

        self._lastAccessed = time.ctime(fstats.st_atime)
        self._lastModified = time.ctime(fstats.st_mtime)


    def isDir(self):
        return self._isDir

    @property
    def name(self):
        return self._name

    def _path(self):
        return self._dir + self.name

    @property
    def permissionsOwner(self):
        return self._permissionsOwner

    @permissionsOwner.setter
    def permissionsOwner(self, permissions):
        self._changePermissions(self._permissionsOwner, permissions, 'u')

    @property
    def permissionsGroup(self):
        return self._permissionsGroup

    @permissionsGroup.setter
    def permissionsGroup(self, permissions):
        self._changePermissions(self._permissionsGroup, permissions, 'g')

    @property
    def permissionsOthers(self):
        return self._permissionsOthers

    @permissionsOthers.setter
    def permissionsOthers(self, permissions):
        self._changePermissions(self._permissionsOthers, permissions, 'o')

    @property
    def groupName(self):
        return self._groupName

    def fileSize(self):
        return self._fileSize

    def lastAccessed(self):
        return self._lastAccessed

    def lastModified(self):
        return self._lastModified

    def _changePermissions(self, oldPerm, newPerm, letter):
        if newPerm[0] != oldPerm[0]:
            try:
                subprocess.run([f'chmod {letter}{"+" if newPerm[0] == "r" else "-"}r', self._path()], check=True)
            except subprocess.CalledProcessError:
                pass

        if newPerm[1] != oldPerm[1]:
            try:
                subprocess.run([f'chmod {letter}{"+" if newPerm[1] == "w" else "-"}w', self._path()], check=True)
            except subprocess.CalledProcessError:
                pass

        oldPerm = newPerm

    @staticmethod
    def _dirSize(path):
        res = os.stat(path).st_size

        if os.path.isdir(path):
            for subDir in os.scandir(path):
                res += FileStats._dirSize(subDir.path)

        return res

    @staticmethod
    def _convertFileSize(size):
        for unit in ['B','KiB','MiB','GiB','TiB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return f"{size:.{2}f}{unit}"

