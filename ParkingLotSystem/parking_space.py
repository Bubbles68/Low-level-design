class ParkingSpace:
    def __init__(self, floor, slot_number, slot_type):
        self.floor = floor
        self.slot_number = slot_number
        self.slot_type = slot_type  # 'Car', 'Bike', 'Truck'
        self.is_occupied = False
        self.vehicle = None

    def park_vehicle(self, vehicle):
        if self.is_occupied:
            return False
        if self.slot_type != vehicle.vehicle_type:
            return False
        self.is_occupied = True
        self.vehicle = vehicle
        return True

    def unpark_vehicle(self):
        if not self.is_occupied:
            return False
        self.is_occupied = False
        self.vehicle = None
        return True

    def __str__(self):
        return f"Slot {self.slot_number} ({self.slot_type}) - {'Occupied' if self.is_occupied else 'Free'}"