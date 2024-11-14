class ParkingTicket:
    def __init__(self, parking_lot_id, floor_no, slot_no, vehicle):
        self.ticket_id = f"{parking_lot_id}_{floor_no}_{slot_no}"
        self.vehicle = vehicle

    def __str__(self):
        return f"Ticket ID: {self.ticket_id}, Vehicle: {self.vehicle}"