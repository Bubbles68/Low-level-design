
'''
Entities:
File - name, extension, size
Directory - list of files, size, addFile
searchParameters - extension,maxSize, name
FileSearcher 
'''
from typing import List, Optional, Callable

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

# Abstract filter class
class FileFilter:
    def matches(self, file: 'File') -> bool:
        raise NotImplementedError("Subclasses must implement matches()")

# Concrete filter implementations
class ExtensionFilter(FileFilter):
    def __init__(self, extension: str):
        self.extension = extension

    def matches(self, file: 'File') -> bool:
        return file.extension == self.extension

class MaxSizeFilter(FileFilter):
    def __init__(self, max_size: int):
        self.max_size = max_size

    def matches(self, file: 'File') -> bool:
        return file.size <= self.max_size

class NamePrefixFilter(FileFilter):
    def __init__(self, prefix: str):
        self.prefix = prefix

    def matches(self, file: 'File') -> bool:
        return file.name.startswith(self.prefix)

# Composite filter to combine multiple criteria
class CompositeFilter(FileFilter):
    def __init__(self):
        self.filters: List[FileFilter] = []

    def add(self, filter: FileFilter) -> None:
        self.filters.append(filter)

    def matches(self, file: 'File') -> bool:
        for filter in self.filters:
            if not filter.matches(file):
                return False
        return True

class FileSearcher:
    def search(self, directory: 'Directory', filter: FileFilter) -> List[File]:
        all_files = directory.getAllFiles()
        return [file for file in all_files if filter.matches(file)]

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

        # Create a composite filter
        search_filter = CompositeFilter()
        search_filter.add(ExtensionFilter("pdf"))
        search_filter.add(MaxSizeFilter(200))
        search_filter.add(NamePrefixFilter("co"))

        # Search
        searcher = FileSearcher()
        results = searcher.search(dir1, search_filter)

        if not results:
            print("No files match the requirements")
        else:
            print(f"Matching files:")
            for file in results:
                print(f"  {file}")

        # Now let's try a different filter (e.g., files with size < 150)
        new_filter = CompositeFilter()
        new_filter.add(MaxSizeFilter(150))

        print("\nFiles with size < 150:")
        results = searcher.search(dir1, new_filter)
        for file in results:
            print(f"  {file}")

if __name__ == "__main__":
    Demo.run()