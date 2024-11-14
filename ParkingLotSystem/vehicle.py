class Vehicle:
    def __init__(self, vehicle_type, reg_number, color):
        self.vehicle_type = vehicle_type  # 'Car', 'Bike', or 'Truck'
        self.reg_number = reg_number
        self.color = color

    def __str__(self):
        return f"{self.vehicle_type} - {self.reg_number} - {self.color}"