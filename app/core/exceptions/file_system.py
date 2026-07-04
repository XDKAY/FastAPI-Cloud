class FileSystemError(Exception):
    """Basic File System Exception"""


class FileSystemIsNotEmptyDirectoryError(FileSystemError):
    """Directory is not empty"""

    def __init__(self, name: str) -> None:
        self.message = f"The directory {name} is not empty."
        
        super().__init__(self.message)


class FileSystemExistingDirectoryError(FileSystemError):
    """Directory already exists"""
    
    def __init__(self, name: str) -> None:
        self.message = f"A directory with that {name} already exists."

        super().__init__(self.message)