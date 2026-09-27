
from collections import deque
from datetime import datetime, timedelta
import math
import uuid

class VehicleType:
    MOTORCYCLE = "MOTORCYCLE"
    COMPACT = "COMPACT"
    LARGE = "LARGE"


class Vehicle:

    def __init__(self, license_plate: str, vehicle_type: str):
        self.license_plate = license_plate.upper().strip()
        self.vehicle_type = vehicle_type.upper().strip()


class ParkingSlot:

    def __init__(self, slot_id: str, vehicle_type: str):
        self.slot_id = slot_id
        self.vehicle_type = vehicle_type
        self.is_occupied = False

    def assign_vehicle(self) -> None:
        self.is_occupied = True

    def release(self) -> None:
        self.is_occupied = False


class Ticket:

    def __init__(self, license_plate: str, slot_id: str, entry_time: datetime = None):
        self.ticket_id = str(uuid.uuid4())[:8].upper()
        self.license_plate = license_plate
        self.slot_id = slot_id
        self.entry_time = entry_time or datetime.now()
        self.exit_time = None
        self.fee = 0.0


class ParkingLot:

    HOURLY_RATES = {
        VehicleType.MOTORCYCLE: 2.00,
        VehicleType.COMPACT: 5.00,
        VehicleType.LARGE: 10.00,
    }

    def __init__(self, capacity_config: dict):
        """
        Initialize parking lot with slot counts per vehicle type.
        Example: capacity_config = {VehicleType.COMPACT: 10, VehicleType.MOTORCYCLE: 5}
        """
        self.slots = {}
        self.available_slots = {
            v_type: deque() for v_type in self.HOURLY_RATES.keys()
        }
        self.active_tickets = {}  # Map: license_plate -> Ticket
        self.completed_tickets = []

        self._initialize_slots(capacity_config)

    def _initialize_slots(self, config: dict) -> None:
        for v_type, count in config.items():
            prefix = v_type[0]
            for i in range(1, count + 1):
                slot_id = f"{prefix}-{i:03d}"
                slot = ParkingSlot(slot_id, v_type)
                self.slots[slot_id] = slot
                self.available_slots[v_type].append(slot_id)

    def get_availability(() -> dict:
        """Returns total and available count per vehicle type."""
        status = {}
        for v_type, available_queue in self.available_slots.items():
            total = sum(1 for s in self.slots.values() if s.vehicle_type == v_type)
            status[v_type] = {
                "available": len(available_queue),
                "total": total
            }
        return status

    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        v_type = vehicle.vehicle_type

        if v_type not in self.available_slots:
            raise ValueError(f"Invalid vehicle type: {v_type}")

        if not self.available_slots[v_type]:
            raise RuntimeError(f"No available slots for vehicle type: {v_type}")

        if vehicle.license_plate in self.active_tickets:
            raise ValueError(f"Vehicle {vehicle.license_plate} is already parked.")

        # Allocate slot
        slot_id = self.available_slots[v_type].popleft()
        self.slots[slot_id].assign_vehicle()

        # Create active ticket
        ticket = Ticket(vehicle.license_plate, slot_id)
        self.active_tickets[vehicle.license_plate] = ticket
        return ticket

    def process_exit(self, license_plate: str, exit_time: datetime = None) -> Ticket:
        plate = license_plate.upper().strip()

        if plate not in self.active_tickets:
            raise KeyError(f"No active ticket found for license plate: {plate}")

        ticket = self.active_tickets.pop(plate)
        ticket.exit_time = exit_time or datetime.now()

        # Fee computation
        slot = self.slots[ticket.slot_id]
        rate = self.HOURLY_RATES[slot.vehicle_type]
        
        duration = ticket.exit_time - ticket.entry_time
        duration_hours = math.ceil(duration.total_seconds() / 3600)
        charged_hours = max(1, duration_hours)  # Minimum 1 hour fee rule
        
        ticket.fee = charged_hours * rate

        # Free resources
        slot.release()
        self.available_slots[slot.vehicle_type].append(slot.slot_id)
        self.completed_tickets.append(ticket)

        return ticket


def main():
    # Setup initial lot capacity
    lot_capacity = {
        VehicleType.MOTORCYCLE: 2,
        VehicleType.COMPACT: 3,
        VehicleType.LARGE: 1,
    }
    parking_lot = ParkingLot(lot_capacity)

    print("=== MODERN PARKING SYSTEM CLI DEMO ===")

    while True:
        print("\n---------------------------------")
        print("1. View Availability")
        print("2. Park Vehicle (Entry)")
        print("3. Exit Vehicle & Pay")
        print("4. Exit System")
        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            print("\n--- Current Availability ---")
            avail = parking_lot.get_availability()
            for v_type, counts in avail.items():
                print(f"{v_type:<12}: {counts['available']}/{counts['total']} free")

        elif choice == "2":
            print("\n--- Vehicle Entry ---")
            plate = input("Enter License Plate: ")
            print("Vehicle Types: 1. MOTORCYCLE  2. COMPACT  3. LARGE")
            t_choice = input("Select Type (1-3): ").strip()
            
            type_map = {"1": VehicleType.MOTORCYCLE, "2": VehicleType.COMPACT, "3": VehicleType.LARGE}
            vehicle_type = type_map.get(t_choice)

            if not vehicle_type:
                print("Error: Invalid vehicle type selection.")
                continue

            try:
                vehicle = Vehicle(plate, vehicle_type)
                ticket = parking_lot.park_vehicle(vehicle)
                print("\n[SUCCESS] Entry Authorized!")
                print(f"Ticket ID   : {ticket.ticket_id}")
                print(f"Assigned Slot: {ticket.slot_id}")
                print(f"Entry Time  : {ticket.entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
            except Exception as e:
                print(f"\n[ERROR] Could not park vehicle: {e}")

        elif choice == "3":
            print("\n--- Vehicle Exit ---")
            plate = input("Enter License Plate: ")
            
            # Simulated time elapsed feature for testing
            simulate_hours = input("Simulate hours spent (Press Enter for real-time): ").strip()
            
            try:
                if simulate_hours:
                    hours = float(simulate_hours)
                    ticket_ref = parking_lot.active_tickets.get(plate.upper().strip())
                    if not ticket_ref:
                        raise KeyError(f"No active ticket found for license plate: {plate}")
                    simulated_exit = ticket_ref.entry_time + timedelta(hours=hours)
                    ticket = parking_lot.process_exit(plate, exit_time=simulated_exit)
                else:
                    ticket = parking_lot.process_exit(plate)

                print("\n[SUCCESS] Exit Processed!")
                print(f"Ticket ID   : {ticket.ticket_id}")
                print(f"Slot Freed  : {ticket.slot_id}")
                print(f"Entry Time  : {ticket.entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Exit Time   : {ticket.exit_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Total Fee   : ${ticket.fee:.2f}")

            except Exception as e:
                print(f"\n[ERROR] Exit failed: {e}")

        elif choice == "4":
            print("\nExiting System. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()