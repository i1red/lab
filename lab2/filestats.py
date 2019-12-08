import os
import grp
import pwd
import time
import stat


class FileStats:
    def __init__(self, path):
        fstats = os.stat(path)
        permissions = stat.filemode(fstats.st_mode)
        self._isDir = permissions[0] == 'd'
        self._permissionsOwner = permissions[1:4]
        self._permissionsGroup = permissions[4:7]
        self._permissionsOthers = permissions[7:]
        self._ownerName = pwd.getpwuid(fstats.st_uid).pw_name
        self._groupName = grp.getgrgid(fstats.st_gid).gr_name
        self._fileSize = FileStats._convertFileSize(FileStats._dirSize(path))
        self._lastAccessed = time.ctime(fstats.st_atime)
        self._lastModified = time.ctime(fstats.st_mtime)


    def isDir(self):
        return self._isDir

    @property
    def permissionsOwner(self):
        return self._permissionsOwner

    @property
    def permissionsGroup(self):
        return self._permissionsOthers

    @property
    def permissionsOthers(self):
        return self._permissionsOthers

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

