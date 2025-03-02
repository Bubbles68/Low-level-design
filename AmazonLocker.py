'''
entities :
Locker - (size-S,M,L , packagePresent, code, id)
Package - (locker number, package id, customer name, size)
customer - (code, package id, name, email)
LockerManagementSystem - (assigns packages to lockers, retreives packages from lockers)
lockerDemo - to run all this
'''
import enum
from tokenize import Double
import uuid
class Customer:
    def __init__(self, packageId:int, name:str, email:str, code:int):
        self.packageId =  packageId
        self.name = name
        self.email = email
        self.code = code

class Size(enum.Enum):
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"

class Locker:
    _lastLockerId=0
    def __init__(self, size:Size):
        self.lockerId='L-'+str(self.generateLockerId())
        self.code = self.generateCode()
        self.size=size
        self.packagePresent=False
        self.package=None

    @classmethod
    def generateLockerId(cls):
        cls._lastLockerId += 1
        return cls._lastLockerId

    def generateCode(self):
        return uuid.uuid4()
    
    def getPackage(self, id, code):
        if self.package.packageId==id and self.code == code:
            self.packagePresent=False
            self.package=None
            return True
        else:
            print(f'Sorry, package not in this locker')
            return False
    
    def assignPackage(self, package):
        if self.packagePresent:
            print(f'Sorry, locker is full / package is present')
            return None
        else:
            self.packagePresent=True
            self.package=package
            print(f'locker is assigned. The locker id is {self.lockerId} and the code is {self.code}')
            return [self.lockerId, self.code]


class Package:
    def __init__(self, packageId:int, customerName: str, size:Size):
        self.packageId = packageId
        self.customerName = customerName
        self.size = size
        self.lockerNumber = ""

class LockerManagementSystem:
    def __init__(self, locationName, numberOfLockers):
        self.locationName=locationName
        self.numberOfLockers = {Size.SMALL: numberOfLockers//3, Size.MEDIUM: numberOfLockers//3, Size.LARGE:numberOfLockers//3}
        self.lockers={}
        self.packagesInLockers={}
        for i in range(numberOfLockers//3):
            locker = Locker(Size.SMALL)
            self.lockers[locker.lockerId] = locker
        for j in range(numberOfLockers//3):
            locker = Locker(Size.MEDIUM)
            self.lockers[locker.lockerId] = locker
        for k in range(numberOfLockers//3):
            locker = Locker(Size.MEDIUM)
            self.lockers[locker.lockerId] = locker

    def assignPackageToLocker(self, package):
        packageSize = package.size
        if self.numberOfLockers[packageSize]!=0:
            for id, locker in self.lockers.items():
                if not locker.packagePresent:
                    lockerId, lockerCode = locker.assignPackage(package)
                    self.numberOfLockers[packageSize]-=1
                    self.packagesInLockers[package.packageId]=[lockerId, lockerCode]
                    print(f'please save the locker Id : {lockerId} and code : {lockerCode}')
                    break
            return
        else:
            print(f'Sorry locker of that size not available')

    def retreivePackage(self, packageId, code):
        code = uuid.UUID(code)
        if packageId in self.packagesInLockers and code==self.packagesInLockers[packageId][1]:
            packageLocker = self.lockers[self.packagesInLockers[packageId][0]]
            retrievedPackage = packageLocker.getPackage(packageId, code)
            if retrievedPackage:
                return True
        else:
            return False
        

class LockerDemo:
    @staticmethod
    def run():
        lockerManager = LockerManagementSystem("Vancouver", 30)
        print(lockerManager.lockers)
        package1 = Package(1, "kavya", Size.SMALL)
        package2 = Package(2, "arvind", Size.MEDIUM)
        package3 = Package(3, "sathya", Size.LARGE)
        package5 = Package(5, "sarada", Size.LARGE)
        lockerManager.assignPackageToLocker(package1)
        lockerManager.assignPackageToLocker(package2)
        lockerManager.assignPackageToLocker(package3)
        print('Please provide packageId', flush=True)
        packageId = int(input())
        print('Please provide code', flush=True)
        code = input()
        if lockerManager.retreivePackage(packageId, code):
            print(f'successfully retreived package : {packageId}')
        else:
            print(f'Wrong package id or Code. Please check again')

if __name__ == "__main__":
    LockerDemo.run()