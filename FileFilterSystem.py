from collections import deque
from typing import List, Protocol
from abc import ABC, abstractmethod

class File:
    def __init__(self, name, file_type, size):
        self.name=name
        self.size=size
        self.file_type=file_type

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size

    def get_date(self):
        return self.date
    
    def get_file_type(self):
        return self.file_type

class Filter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def matches(self, file:str) -> bool:
        pass

class FileNameFilter(Filter):
    def __init__(self, name):
        self.name=name
    def matches(self, file):
        return file.get_name()==self.name

class FileTypeFilter(Filter):
    def __init__(self, extension):
        self.extension=extension
    def matches(self,file):
        return file.get_file_type() == self.extension
    
class FileSizeFilter(Filter):
    def __init__(self, min_size: int=0, max_size:int=float('inf')):
        self.min_size = min_size
        self.max_size = max_size
    def matches(self, file) -> bool:
        return self.min_size <= file.get_size() <= self.max_size
    
class Search:
    def __init__(self, files, filters, condition="OR"):
        self.files = files
        self.filters = [globals()[filter_name](*args) for filter_name, args in filters.items()]
        self.condition = condition  # "AND" or "OR"

    def find_files(self):
        result = []
        for file in self.files:
            matches = [filter.matches(file) for filter in self.filters]
            if (self.condition == "AND" and all(matches)) or (self.condition == "OR" and any(matches)):
                result.append(file.get_name())

        if len(result)==0:
            return "No files with specified filters found"
        return result

# --- TEST CASE ---
if __name__ == "__main__":
    # Create sample files
    files = [
        File("report", "pdf", 50),
        File("notes", "txt", 10),
        File("script", "py", 5),
        File("design", "txt", 100),
        File("music", "mp3", 500),
    ]

    # Define filters: Looking for .txt or .py files
    filters = {
        "FileTypeFilter": ("txt",),
        "FileSizeFilter":(10,100)
    }

    # Create search and find files
    search = Search(files, filters, "AND")
    result = search.find_files()
    print(result)
