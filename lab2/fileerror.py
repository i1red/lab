class FileSystemError(Exception):
    pass


class CopyFileError(FileSystemError):
    pass


class RenameFileError(FileSystemError):
    pass


class OpenFileError(FileSystemError):
    pass


class DeleteFileError(FileSystemError):
    pass


class MoveFileError(FileSystemError):
    pass


class MoveToTrashError(FileSystemError):
    pass


class CreateFolderError(FileSystemError):
    pass


class CreateFileError(FileSystemError):
    pass