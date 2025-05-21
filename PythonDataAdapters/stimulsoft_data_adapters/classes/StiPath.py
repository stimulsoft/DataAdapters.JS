"""
Stimulsoft.Reports.JS
Version: 2025.2.4
Build date: 2025.05.19
License: https://www.stimulsoft.com/en/licensing/reports
"""

import os

import requests


class StiPath:

### Fields

    filePath: str = None
    """The full path to the file, if the file exists."""

    directoryPath: str = None
    """The full path to the file directory, if the file exists."""

    fileName: str = None
    """The file name."""

    fileNameOnly: str = None
    """The file name without the extension."""

    fileExtension: str = None
    """The file extension."""

    fileUrl: str = None
    """The URL to the file, if the file exists (code 200 was received when requesting the file)."""


### Helpers

    def normalize(path: str) -> str:
        return os.path.normpath((path or '').split('?')[0]).rstrip('/\\')
    
    def __isUrl(path: str) -> bool:
        return path != None and (path.startswith('http://') or path.startswith('https://'))
    
    def __getMissingFileName(filePath: str) -> str:
        filePath = StiPath.normalize(filePath)
        return os.path.basename(filePath)
    
    def __getRealFilePath(filePath: str) -> str:
        if StiPath.__isUrl(filePath):
            try:
                headers = requests.head(filePath)
            except Exception as e:
                return None
            
            return filePath if headers.status_code == 200 else None

        filePath = StiPath.normalize(filePath)
        if os.path.isfile(filePath):
            return filePath
        
        workingDir = os.getcwd()
        filePath = StiPath.normalize(f'{workingDir}/{filePath}')
        if os.path.isfile(filePath):
            return filePath
        
        return None
    
    def __getRealDirectoryPath(directoryPath: str) -> str:
        if StiPath.__isUrl(directoryPath):
            return None

        filePath = StiPath.normalize(directoryPath)
        
        directoryPath = filePath
        if os.path.isdir(directoryPath):
            return directoryPath

        workingDir = os.getcwd()
        directoryPath = StiPath.normalize(f'{workingDir}/{directoryPath}')
        if os.path.isdir(directoryPath):
            return directoryPath
        
        directoryPath = os.path.dirname(filePath)
        if os.path.isdir(directoryPath):
            return directoryPath

        directoryPath = StiPath.normalize(f'{workingDir}/{directoryPath}')
        if os.path.isdir(directoryPath):
            return directoryPath
        
        return None


### Constructor

    def __init__(self, filePath):
        self.filePath = StiPath.__getRealFilePath(filePath)
        self.directoryPath = StiPath.__getRealDirectoryPath(filePath)
        if self.filePath != None and StiPath.__isUrl(filePath):
            self.fileUrl = self.filePath
        
        self.fileName = os.path.basename(self.filePath) if self.filePath != None else StiPath.__getMissingFileName(filePath)
        if self.filePath == None and (self.directoryPath or '').endswith(self.fileName):
            self.fileName = None

        if self.fileName != None:
            self.fileNameOnly, self.fileExtension = os.path.splitext(self.fileName)
            self.fileExtension = self.fileExtension[1:].lower() if len(self.fileExtension or '') > 1 else ''