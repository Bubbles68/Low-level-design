import enum
import time

class Request:
    def __init__(self, currentFloor, destFloor):
        self.currentFloor = currentFloor
        self.destFloor = destFloor

class Elevator:
    def __init__(self, id: int, capacity: int) -> None:
        self.direction = Direction.UP
        self.currentFloor = 1
        self.id = id
        self.requests = []
        self.capacity = capacity

    def addRequest(self, request: Request) -> None:
        if len(self.requests) < self.capacity:
            self.requests.append(request)
            print(f'Request sent to elevator {self.id}: Source Floor {request.currentFloor} to Destination Floor {request.destFloor}')

    def getNextRequest(self) -> Request:
        if self.requests:
            return self.requests.pop(0)
        return None

    def processRequest(self, request: Request) -> None:
        if not request:
            return
        start = self.currentFloor
        end = request.destFloor
        if start < end:
            self.direction = Direction.UP
            for i in range(start, end + 1):
                print(f'Elevator {self.id} moving up to floor {i}')
                time.sleep(0.5)
        elif start > end:
            self.direction = Direction.DOWN
            for i in range(start, end - 1, -1):
                print(f'Elevator {self.id} moving down to floor {i}')
                time.sleep(0.5)
        else:
            print(f'Elevator {self.id} already at floor {request.destFloor}')
        self.currentFloor = request.destFloor

    def processRequests(self) -> None:
        while self.requests:
            request = self.getNextRequest()
            self.processRequest(request)

    def run(self) -> None:
        self.processRequests()

class Direction(enum.Enum):
    UP = 1
    DOWN = -1

class ElevatorController:
    def __init__(self, numElevators: int, capacity: int) -> None:
        self.elevators = []
        for i in range(numElevators):
            self.elevators.append(Elevator(i, capacity))

    def findOptimalElevator(self, sourceFloor: int) -> Elevator:
        minDist = float('inf')
        optimalElevator = None
        for elevator in self.elevators:
            distance = abs(elevator.currentFloor - sourceFloor)
            # Check if elevator has capacity and is closer
            if distance < minDist and len(elevator.requests) < elevator.capacity:
                minDist = distance
                optimalElevator = elevator
        # If no elevator has capacity, return the one with least requests
        if optimalElevator is None:
            optimalElevator = min(self.elevators, key=lambda e: len(e.requests))
        return optimalElevator

    def requestElevator(self, sourceFloor: int, destFloor: int) -> None:
        optimalElevator = self.findOptimalElevator(sourceFloor)
        request = Request(sourceFloor, destFloor)
        optimalElevator.addRequest(request)
        optimalElevator.processRequests()  # Process the request immediately

class ElevatorDemo:
    @staticmethod
    def run():
        controller = ElevatorController(2, 3)  # 2 elevators, capacity 3
        print("Starting elevator demo...")
        time.sleep(1)
        controller.requestElevator(10, 12)  # Should use elevator 0
        time.sleep(1)
        controller.requestElevator(1, 7)    # Should use elevator 0
        time.sleep(1)
        controller.requestElevator(2, 1)    # Should use elevator 1

if __name__ == "__main__":
    ElevatorDemo.run()