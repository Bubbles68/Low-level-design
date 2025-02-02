from enum import Enum
from datetime import datetime
import uuid

class VehicleType(Enum):
    CAR = "Car"
    BIKE = "Bike"
    TRUCK = "Truck"

class ParkingSpot:
    def __init__(self, spot_id: int, spot_type: VehicleType):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_occupied = False
        self.vehicle = None

    def park_vehicle(self, vehicle):
        if not self.is_occupied and vehicle.vehicle_type == self.spot_type:
            self.vehicle = vehicle
            self.is_occupied = True
            return True
        return False

    def remove_vehicle(self):
        self.vehicle = None
        self.is_occupied = False

class Vehicle:
    def __init__(self, plate_number: str, vehicle_type: VehicleType):
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type

class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()

    def get_ticket_info(self):
        return {
            "ticket_id": self.ticket_id,
            "vehicle_plate": self.vehicle.plate_number,
            "spot_id": self.spot.spot_id,
            "entry_time": self.entry_time,
        }

class ParkingLot:
    def __init__(self, num_spots):
        self.spots = {
            VehicleType.CAR: [],
            VehicleType.BIKE: [],
            VehicleType.TRUCK: []
        }
        spot_id = 1
        for vt in self.spots.keys():
            for _ in range(num_spots[vt]):
                self.spots[vt].append(ParkingSpot(spot_id, vt))
                spot_id += 1
        self.active_tickets = {}
  
    def park_vehicle(self, vehicle: Vehicle):
        for spot in self.spots[vehicle.vehicle_type]:
            if not spot.is_occupied:
                if spot.park_vehicle(vehicle):
                    ticket = Ticket(vehicle, spot)
                    self.active_tickets[ticket.ticket_id] = ticket
                    return ticket.get_ticket_info()
        return "No available spots"

    def exit_vehicle(self, ticket_id: str):
        ticket = self.active_tickets.get(ticket_id)
        if ticket:
            ticket.spot.remove_vehicle()
            del self.active_tickets[ticket_id]
            return f"Vehicle {ticket.vehicle.plate_number} exited. Spot {ticket.spot.spot_id} freed."
        return "Invalid ticket ID"

# Example usage
if __name__ == "__main__":
    parking_lot = ParkingLot({VehicleType.CAR: 2, VehicleType.BIKE: 2, VehicleType.TRUCK: 1})
    
    car = Vehicle("DKV 992", VehicleType.CAR)
    car2 = Vehicle("TKM 429", VehicleType.CAR)

    ticket_info = parking_lot.park_vehicle(car)
    ticket_info2 = parking_lot.park_vehicle(car2)

    print(ticket_info)
    print(ticket_info2)
    
