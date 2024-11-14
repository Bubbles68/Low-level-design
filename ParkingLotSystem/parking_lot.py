from parking_space import ParkingSpace
from parking_ticket import ParkingTicket

class ParkingLot:
    def __init__(self, parking_lot_id):
        self.parking_lot_id = parking_lot_id
        self.floors = []

    def add_floor(self, floor_number, car_slots, bike_slots, truck_slots):
        floor = {
            'floor_number': floor_number,
            'slots': []
        }
        # Add truck slot
        for i in range(truck_slots):
            floor['slots'].append(ParkingSpace(floor_number, i + 1, 'Truck'))
        # Add bike slots
        for i in range(truck_slots, truck_slots + bike_slots):
            floor['slots'].append(ParkingSpace(floor_number, i + 1, 'Bike'))
        # Add car slots
        for i in range(truck_slots + bike_slots, car_slots + truck_slots + bike_slots):
            floor['slots'].append(ParkingSpace(floor_number, i + 1, 'Car'))

        self.floors.append(floor)

    def park_vehicle(self, vehicle):
        # Find first available slot based on rules
        for floor in self.floors:
            for slot in floor['slots']:
                if not slot.is_occupied and slot.slot_type == vehicle.vehicle_type:
                    slot.park_vehicle(vehicle)
                    ticket = ParkingTicket(self.parking_lot_id, floor['floor_number'], slot.slot_number, vehicle)
                    return ticket
        return None

    def unpark_vehicle(self, ticket):
        ticket_info = ticket.ticket_id.split('_')
        floor_number = int(ticket_info[1])
        slot_number = int(ticket_info[2])

        for floor in self.floors:
            if floor['floor_number'] == floor_number:
                for slot in floor['slots']:
                    if slot.slot_number == slot_number:
                        if slot.unpark_vehicle():
                            return f"Vehicle {ticket.vehicle.reg_number} unparked successfully."
                        else:
                            return f"Slot {slot_number} is already free."
        return "Ticket is invalid or already used."

    def display_free_slots(self, vehicle_type):
        for floor in self.floors:
            print(f"Floor {floor['floor_number']} - Free Slots for {vehicle_type}:")
            for slot in floor['slots']:
                if slot.slot_type == vehicle_type and not slot.is_occupied:
                    print(slot)

    def display_occupied_slots(self, vehicle_type):
        for floor in self.floors:
            print(f"Floor {floor['floor_number']} - Occupied Slots for {vehicle_type}:")
            for slot in floor['slots']:
                if slot.slot_type == vehicle_type and slot.is_occupied:
                    print(slot)