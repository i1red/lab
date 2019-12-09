import os
import grp
import pwd
import time
import stat
import filecommands


class FileStats:
    def __init__(self, path):
        fstats = os.stat(path)
        permissions = stat.filemode(fstats.st_mode)
        splitPath = path.split('/')

        self._name = splitPath[-1]
        splitPath.pop()
        self._dir = '/'.join(splitPath) + ('/' if len(splitPath) > 0 else '')

        self._isDir = permissions[0] == 'd'
        self._permissions = permissions[1:]
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

    @name.setter
    def name(self, newName):
        newPath = self._dir + newName
        filecommands.rename(self._path(), newPath)

    def _path(self):
        return self._dir + self.name

    @property
    def permissions(self):
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        if self.permissions != permissions:
            mode = '0o'
            for perm in [permissions[:3], permissions[3:6], permissions[6:]]:
                tmp = 0
                for i, sym in enumerate(reversed(perm)):
                    if sym != '-':
                        tmp += 2 ** i
                mode += str(tmp)
            os.chmod(self._path(), int(mode, 8))

    def setPermissions(self, owner, group, others):
        newPermissions = owner + self.permissions[2] + group + self.permissions[5] + others + self.permissions[8]
        self.permissions = newPermissions

    @property
    def groupName(self):
        return self._groupName

    def fileSize(self):
        return self._fileSize

    def lastAccessed(self):
        return self._lastAccessed

    def lastModified(self):
        return self._lastModified

    @staticmethod
    def _dirSize(path):
        res = os.stat(path).st_size

        if os.path.isdir(path):
            for subDir in os.scandir(path):
                if os.path.exists(subDir.path) and os.access(subDir.path, os.R_OK) and not os.path.islink(path):
                    res += FileStats._dirSize(subDir.path)

        return res

    @staticmethod
    def _convertFileSize(size):
        for unit in [' B',' KiB',' MiB',' GiB',' TiB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return f"{size:.{2}f}{unit}"


