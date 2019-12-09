import os
import grp
import pwd
import time
import stat
import subprocess


class FileStats:
    def __init__(self, path):
        fstats = os.stat(path)
        permissions = stat.filemode(fstats.st_mode)
        splitPath = path.split('/')

        self._name = splitPath[-1]
        splitPath.pop()
        self._dir = '/' + '/'.join(splitPath) + ('/' if len(splitPath) > 0 else '')

        self._isDir = permissions[0] == 'd'
        self._permissionsOwner = tuple(permissions[1:4])
        self._permissionsGroup = tuple(permissions[4:7])
        self._permissionsOthers = tuple(permissions[7:])

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
        if permissions != self._permissionsOwner:
            try:
                subprocess.run([f'chmod u+{"".join(permissions)}', self._path()], check=True)
            except subprocess.CalledProcessError:
                pass

    @property
    def permissionsGroup(self):
        return self._permissionsGroup

    @permissionsGroup.setter
    def permissionsGroup(self, permissions):
        if permissions != self._permissionsGroup:
            try:
                subprocess.run([f'chmod g+{"".join(permissions)}', self._path()], check=True)
            except subprocess.CalledProcessError:
                pass

    @property
    def permissionsOthers(self):
        return self._permissionsOthers

    @permissionsOthers.setter
    def permissionsOthers(self, permissions):
        if permissions != self._permissionsOthers:
            try:
                subprocess.run([f'chmod o+{"".join(permissions)}', self._path()], check=True)
            except subprocess.CalledProcessError:
                pass

    @property
    def groupName(self):
        return self._groupName

    @property
    def fileSize(self):
        return self._fileSize

    @property
    def lastAccessed(self):
        return self._lastAccessed

    @property
    def lastModified(self):
        return self._lastModified

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

