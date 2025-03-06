from abc import ABC, abstractmethod
import os
from enum import Enum
from typing import List

class FileRule(ABC):
    @abstractmethod
    def match(self, file_path: str) -> bool:
        pass

class FileRuleExtension(FileRule):
    def __init__(self, ext: str):
        self.ext = ext

    def match(self, file_path: str) -> bool:
        result = file_path.endswith("." + self.ext)
        print(f"Checking {file_path} for extension .{self.ext}: {result}")
        return result
    
class FileRuleSizeOp(Enum):
        LT = "<"
        LTE = "<="
        EQ = "=="
        GT = ">"
        GTE = ">="

class FileRuleSize(FileRule):

    def __init__(self, size: int, op: 'FileRuleSize.FileRuleSizeOp'):
        self.size = size
        self.op = op

    def match(self, file_path: str) -> bool:
        file_size = os.path.getsize(file_path)
        if self.op == self.FileRuleSizeOp.LT:
            return file_size < self.size
        elif self.op == self.FileRuleSizeOp.LTE:
            return file_size <= self.size
        elif self.op == self.FileRuleSizeOp.EQ:
            return file_size == self.size
        elif self.op == self.FileRuleSizeOp.GT:
            return file_size > self.size
        elif self.op == self.FileRuleSizeOp.GTE:
            return file_size >= self.size
        return False

class FileRuleAnd(FileRule):
    def __init__(self, *rules: FileRule):
        self.and_rules = list(rules)

    def match(self, file_path: str) -> bool:
        return all(rule.match(file_path) for rule in self.and_rules)

class FileRuleOr(FileRule):
    def __init__(self, *rules: FileRule):
        self.or_rules = list(rules)

    def match(self, file_path: str) -> bool:
        return any(rule.match(file_path) for rule in self.or_rules)

def find(dir_path: str, rule: FileRule) -> None:
    print(f"Scanning directory: {dir_path}")
    if not os.path.exists(dir_path):
        print(f"Error: Directory {dir_path} does not exist")
        return
    if not os.path.isdir(dir_path):
        print(f"Error: {dir_path} is not a directory")
        return
        
    try:
        files = os.listdir(dir_path)
        print(f"Found {len(files)} items in directory")
        for filename in files:
            full_path = os.path.join(dir_path, filename)
            print(f"Checking: {full_path}")
            if os.path.isfile(full_path):
                if rule.match(full_path):
                    print(f"Match found: {filename}")
            else:
                print(f"Skipping {filename} (not a file)")
        if not files:
            print("No files found in directory")
    except PermissionError:
        print(f"Error: Permission denied to access {dir_path}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    dir_path = "/Users/kavyagarikapati/Desktop/Repo/Low-Level-Design"
    rule = FileRuleOr(FileRuleExtension("py"))
    find(dir_path, rule)