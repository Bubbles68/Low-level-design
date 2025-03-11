
'''
Entities:
File - name, extension, size
Directory - list of files, size, addFile
searchParameters - extension,maxSize, name
FileSearcher 
'''

from typing import List, Optional

class File:
    def __init__(self, name, extension, size):
        self.name = name
        self.extension = extension
        self.size = size

    def __str__(self):
        return f"{self.name}.{self.extension} ({self.size} bytes)"

class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.directories = []
        self.size = 0

    def addFile(self, file: 'File') -> None:
        self.files.append(file)
        self.size += file.size

    def addDirectory(self, directory: 'Directory') -> None:
        self.directories.append(directory)
        self.size += directory.size

    def getAllFiles(self) -> List[File]:
        all_files = self.files.copy()
        for sub_dir in self.directories:
            all_files.extend(sub_dir.getAllFiles())
        return all_files

class SearchParams:
    def __init__(self, extension: Optional[str] = None, max_size: Optional[int] = None, name: Optional[str] = None):
        self.extension = extension
        self.max_size = max_size
        self.name = name

class FileSearcher:
    def search(self, directory: 'Directory', params: 'SearchParams') -> List[File]:
        all_files = directory.getAllFiles()
        matching_files = []
        for file in all_files:
            if self.checkFilter(file, params):
                matching_files.append(file)
        return matching_files
    
    def checkFilter(self, file: 'File', params: 'SearchParams') -> bool:
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
        # Files
        file1 = File("System Design Intro", "pdf", 100)
        file2 = File("code LLD intro", "pdf", 200)
        file3 = File("code basics", "pdf", 50)

        # Subdirectory
        sub_dir = Directory("coding practice")
        sub_dir.addFile(file3)

        # Main directory
        dir1 = Directory("Amazon prep")
        dir1.addFile(file1)
        dir1.addFile(file2)
        dir1.addDirectory(sub_dir)

        # Search
        params = SearchParams(extension="pdf", max_size=200, name="co")
        searcher = FileSearcher()
        results = searcher.search(dir1, params)
        
        if not results:
            print("No files match the requirements")
        else:
            print(f"Matching files:")
            for file in results:
                print(f"  {file}")

if __name__ == "__main__":
    Demo.run()