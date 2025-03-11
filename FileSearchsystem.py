'''
Entities:
File - name, extension, size
Directory - list of files, size, addFile
searchParameters - extension,maxSize, name
FileSearcher 
'''

from abc import abstractmethod
from typing import List, Optional


class File:
    def __init__(self, name, extension, size):
        self.name=name
        self.extension=extension
        self.size=size
class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.size = 0

    def addFile(self, file):
        if file in self.files:
            print(f"file with the name {file.name} exists. Do you want to replace?")
        self.files.append(file)
        self.size += file.size

    def getAllFiles(self):
        return self.files

class SearchParams:
    def __init__(self, extension: Optional[str] = None, max_size: Optional[int] = None, name:Optional[str] = None):
        self.extension = extension
        self.max_size = max_size
        self.name = name

class FileSearcher:
    def search(self, directory, params):
        allFiles = directory.getAllFiles()
        matchingFiles = []
        for file in allFiles:
            if self.checkFilter(file, params):
                matchingFiles.append(file)
        return matchingFiles
    
    def checkFilter(self, file, params):
        if params.extension and file.extension != params.extension:
            return False
        if params.max_size and file.size > params.max_size:
            return False
        if params.name and not file.name.startswith(params.name):
            return False
        return True
    
class Demo:
    @staticmethod
    def run():
        file1 = File("System Design Intro", "pdf", 100)
        file2 = File("code LLD intro", "pdf", 200)
        file3 = File("code basics", "pdf", 50)

        dir1 = Directory("Amazon prep")
        dir1.addFile(file1)
        dir1.addFile(file2)
        dir1.addFile(file3)

        dir1.getAllFiles()
        params = SearchParams(extension="pdf", max_size=200, name = "co")
        searcher = FileSearcher()
        results = searcher.search(dir1, params)
        if len(results)==0:
            print(f"no files match the requirements")
        for file in results:
            print(file.name)

if __name__=="__main__":
    Demo.run()