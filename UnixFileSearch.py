class File:
    def __init__(self, name, extension, size):
        self.name = name
        self.extension = extension
        self.size = size

class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.subdirs = []

    def add_file(self, file):
        self.files.append(file)
    
    def add_directory(self, dir):
        self.subdirs.append(dir)

class SearchParams:
    def __init__(self, extension=None, max_size=None, name=None):
        self.extension = extension
        self.max_size = max_size
        self.name = name

class FileSearcher:
    def search(self, directory, params):
        matching_files = []
        # Check current directory's files
        for file in directory.files:
            if self._matches(file, params):
                matching_files.append(file)
        # Recursively search subdirectories
        for subdir in directory.subdirs:
            matching_files.extend(self.search(subdir, params))
        return matching_files
    
    def _matches(self, file, params):
        if params.extension and file.extension != params.extension:
            return False
        if params.max_size and file.size > params.max_size:
            return False
        if params.name and not file.name.startswith(params.name):
            return False
        return True

# Demo
dir1 = Directory("root")
dir1.add_file(File("test", "txt", 100))
sub_dir = Directory("sub")
sub_dir.add_file(File("code", "py", 50))
dir1.add_directory(sub_dir)
searcher = FileSearcher()
results = searcher.search(dir1, SearchParams(extension="py"))
for file in results:
    print(file.name)  # Outputs: "code"