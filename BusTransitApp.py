from typing import Dict, Tuple
from math import sqrt

class TransitError(Exception):
    pass

class Location:
    def __init__(self, x: float, y: float):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise ValueError("Coordinates must be numbers")
        self.x = x
        self.y = y

    def get_coordinates(self) -> Tuple[float, float]:
        return (self.x, self.y)

class Bus:
    def __init__(self, bus_id: int, capacity: int, source: Location, dest: Location, speed: float):
        if speed <= 0 or capacity <= 0:
            raise TransitError("Speed and capacity must be positive")
        self.bus_id = bus_id
        self.capacity = capacity
        self.source = source
        self.destination = dest
        self.speed = speed
        self.current_location = source
        self._passengers = 0  # Track occupancy

    def update_location(self, x: float, y: float):
        self.current_location = Location(x, y)

    def has_capacity(self) -> bool:
        return self._passengers < self.capacity

    def add_passenger(self):
        if not self.has_capacity():
            raise TransitError(f"Bus {self.bus_id} is full")
        self._passengers += 1

class Customer:
    def __init__(self, cust_id: int, name: str, email: str, location: Location):
        self.cust_id = cust_id
        self.name = name
        self.email = email
        self.location = location

class TransitManager:
    def __init__(self):
        self.buses: Dict[int, Bus] = {}

    def add_bus(self, bus: Bus):
        if bus.bus_id in self.buses:
            raise TransitError(f"Bus {bus.bus_id} already exists")
        self.buses[bus.bus_id] = bus

    def remove_bus(self, bus: Bus):
        if bus.bus_id not in self.buses:
            raise TransitError(f"Bus {bus.bus_id} not found")
        del self.buses[bus.bus_id]

    def get_location_of_bus(self, bus_id: int) -> Tuple[float, float]:
        if bus_id not in self.buses:
            raise TransitError(f"Bus {bus_id} not found")
        return self.buses[bus_id].current_location.get_coordinates()

    def find_nearest_bus(self, cust_loc: Tuple[float, float]) -> Tuple[int, float]:
        if not self.buses:
            raise TransitError("No buses available")
        min_dist = float('inf')
        nearest_bus_id = None
        for bus in self.buses.values():
            if not bus.has_capacity():
                continue  # Skip full buses
            bus_loc = bus.current_location.get_coordinates()
            dist = sqrt((bus_loc[0] - cust_loc[0])**2 + (bus_loc[1] - cust_loc[1])**2)
            if dist < min_dist:
                min_dist = dist
                nearest_bus_id = bus.bus_id
        if nearest_bus_id is None:
            raise TransitError("No available buses with capacity")
        print(f"Nearest bus: Bus {nearest_bus_id}, {min_dist} km away")
        return (nearest_bus_id, min_dist)

    def time_to_reach_customer(self, cust_loc: Tuple[float, float]) -> float:
        bus_id, dist = self.find_nearest_bus(cust_loc)
        time = dist / self.buses[bus_id].speed  # Time in hours
        print(f"Time to reach customer: {time:.2f} hours")
        return time

class TransitAppDemo:
    @staticmethod
    def run():
        # Create buses
        bus1 = Bus(1, 2, Location(0, 0), Location(20, 20), 40)
        bus2 = Bus(2, 1, Location(10, 10), Location(25, 25), 50)
        bus3 = Bus(3, 3, Location(15, 0), Location(67, 76), 60)

        # Customers
        cust1 = Customer(10, "Kavya", "kay@gmail.com", Location(30, 20))
        cust2 = Customer(20, "Arvind", "arvi@gmail.com", Location(40, 50))

        # Transit manager
        manager = TransitManager()
        manager.add_bus(bus1)
        manager.add_bus(bus2)
        manager.add_bus(bus3)

        # Update location and add passengers
        bus1.update_location(15, 15)
        bus2.add_passenger()  # Bus 2 is now full (capacity 1)

        # Test functionality
        print("Bus 1 location:", manager.get_location_of_bus(1))
        manager.time_to_reach_customer(cust1.location.get_coordinates())
        manager.time_to_reach_customer(cust2.location.get_coordinates())

if __name__ == "__main__":
    TransitAppDemo.run()