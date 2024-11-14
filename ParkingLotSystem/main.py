# main.py
from parking_lot import ParkingLot
from vehicle import Vehicle
from parking_ticket import ParkingTicket

class ParkingLotCLI:
    def __init__(self):
        self.parking_lot = None

    def create_parking_lot(self):
        lot_id = input("Enter Parking Lot ID: ")
        self.parking_lot = ParkingLot(lot_id)
        print(f"Parking lot {lot_id} created.")

    def add_floor(self):
        if not self.parking_lot:
            print("Please create a parking lot first.")
            return
        floor_no = int(input("Enter floor number: "))
        car_slots = int(input("Enter number of car slots: "))
        bike_slots = int(input("Enter number of bike slots: "))
        truck_slots = int(input("Enter number of truck slots: "))
        self.parking_lot.add_floor(floor_no, car_slots, bike_slots, truck_slots)
        print(f"Floor {floor_no} added.")

    def park_vehicle(self):
        if not self.parking_lot:
            print("Please create a parking lot first.")
            return
        vehicle_type = input("Enter vehicle type (Car/Bike/Truck): ")
        reg_number = input("Enter vehicle registration number: ")
        color = input("Enter vehicle color: ")
        vehicle = Vehicle(vehicle_type, reg_number, color)
        ticket = self.parking_lot.park_vehicle(vehicle)
        if ticket:
            print(f"Vehicle parked successfully. Ticket ID: {ticket}")
        else:
            print("No available parking slot for this vehicle type.")

    def unpark_vehicle(self):
        if not self.parking_lot:
            print("Please create a parking lot first.")
            return
        ticket_id = input("Enter ticket ID: ")
        ticket_info = ticket_id.split('_')
        floor_no = int(ticket_info[1])
        slot_no = int(ticket_info[2])
        ticket = ParkingTicket(self.parking_lot.parking_lot_id, floor_no, slot_no, None)
        message = self.parking_lot.unpark_vehicle(ticket)
        print(message)

    def display_free_slots(self):
        if not self.parking_lot:
            print("Please create a parking lot first.")
            return
        vehicle_type = input("Enter vehicle type (Car/Bike/Truck): ")
        self.parking_lot.display_free_slots(vehicle_type)

    def display_occupied_slots(self):
        if not self.parking_lot:
            print("Please create a parking lot first.")
            return
        vehicle_type = input("Enter vehicle type (Car/Bike/Truck): ")
        self.parking_lot.display_occupied_slots(vehicle_type)

    def print_menu(self):
        print("\n=== Parking Lot System ===")
        print("1. Create Parking Lot")
        print("2. Add Floors to Parking Lot")
        print("3. Park Vehicle")
        print("4. Unpark Vehicle")
        print("5. Display Free Slots by Vehicle Type")
        print("6. Display Occupied Slots by Vehicle Type")
        print("7. Exit")

    def run(self):
        while True:
            self.print_menu()
            choice = input("Enter your choice: ")
            action_map = {
                '1': self.create_parking_lot,
                '2': self.add_floor,
                '3': self.park_vehicle,
                '4': self.unpark_vehicle,
                '5': self.display_free_slots,
                '6': self.display_occupied_slots,
                '7': self.exit_application
            }
            action = action_map.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please try again.")

    def exit_application(self):
        print("Exiting... Goodbye!")
        exit()

if __name__ == "__main__":
    cli = ParkingLotCLI()
    cli.run()
