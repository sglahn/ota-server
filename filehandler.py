#!/usr/bin/env python3

import os
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

class FileHandler:
    def __init__(self, availableFirmwares={}, filePatterns=[r".*"]):
        self.firmwares = availableFirmwares
        self.watcher = self.FileWatcher(regexes=filePatterns, ignore_directories=True)

    def getFirmwareName(self, path):
        fileName = os.path.basename(path)
        return fileName[:fileName.index('-')]

    def getFirmwareVersion(self, path):
        fileName = os.path.basename(path)
        return fileName[fileName.index('-') +1:fileName.index('.bin')]

    class FileWatcher(RegexMatchingEventHandler):

        def on_created(self, event):
            name = self.FileHandler.getFirmwareName(event.src_path)
            version = self.getFirmwareVersion(event.src_path)
            if name in FileHandler.firmwares:
                currentVersions = firmwares[name]
                if version not in currentVersions:
                    currentVersions.append(version)
                    firmwares[name] = sorted(currentVersions, reverse=True)
                else:
                    firmwares[name] = [version]
            print(firmwares)

        def on_deleted(self, event):    
            name = self.getFirmwareName(event.src_path)
            version = self.getFirmwareVersion(event.src_path)
            if name in FileHandler.firmwares:
                firmwares[name].remove(version)
                if len(firmwares[name]) == 0:
                    del firmwares[name]
            print(firmwares)

