#parking_system

An object-oriented, high-performance parking management system designed to handle vehicle entry, exit processing, fee calculation, and real-time availability tracking.

---

## 1. Algorithms & Workflows

### 1.1 Vehicle Entry Algorithm
1. the system takes the cars plate number and the type of vehicle when it approaches the gate. `license_plate` and `vehicle_type`.
2. the system checks available slots and indicates using a colour-specific indicator light. `vehicle_type`.
   - If `available_slots == 0`, red light to indicate  error and abort workflow.
3. the system then allocates space to each car
   - Retrieve an available `Slot` object.
   - Update `Slot.is_occupied = True`.
4. it creates a ticket which authorises entrance.
   - Instantiate `Ticket` object with unique `ticket_id`, `license_plate`, `slot_id`, and `entry_timestamp = CurrentTime()`.
5. starts time calculations.
   - Store active ticket in key-value lookup (`active_tickets[license_plate] = Ticket`).
   - Decrement total available capacity for the specified vehicle type.
6.system  Issues ticket to vehicle driver displaying `ticket_id`, assigned `slot_id`, and `entry_timestamp`.

### 1.2 Vehicle Exit Algorithm
1. car requests exit: Input `license_plate` (or `ticket_id`).
2. system checks out the car records.
   - Query `active_tickets` hash map using `license_plate`.
   - If record does not exist, display **"Active Ticket Not Found"** error and abort workflow.
3. The system calculates total duration.
   - Fetch `entry_timestamp`.
   - Record `exit_timestamp = CurrentTime()`.
   - Compute `duration_hours = ceil((exit_timestamp - entry_timestamp) / 3600)`.
   - Apply minimum billing rule: `charged_hours = max(1, duration_hours)`.
4. system calculates total fee due.
   - Retrieve hourly rate $R$ corresponding to vehicle type.
   - Compute total fee: $\text{Fee} = \text{charged\_hours} \times R$.
5. system releases the car 
   - Update assigned `Slot.is_occupied = False`.
   - Increment available capacity for the specified vehicle type.
   - Remove ticket from `active_tickets` map and record transaction in historical logs.
6. output: Present fee summary showing total time spent, hourly rate, and total fee due.

---

## 2. Data Structures & Complexity Analysis

| Data Structure | Use Case / Application | Time Complexity | Justification |
| :--- | :--- | :--- | :--- |
hash map (`dict`) | `active_tickets` mapping `license_plate -> Ticket` | Average Lookups / Insertions / Deletions | Guarantees instant lookup during vehicle exit regardless of total system scale. |
|  (`dict`) | `slots` mapping `slot_id -> Slot` | Direct Access | Provides instantaneous slot state updates and lookup by identifier. |
| **List / Queue (`deque`) | Available slot tracking per vehicle type | Insertion & Removal | Efficient tracking and assignment of the next available parking slot. |
|  | `Vehicle`, `Slot`, `Ticket`, `ParkingLot` | Encapsulation | Encapsulates domain logic, enforces clean interfaces, and maintains strong system state integrity. |

---

## 3. Database Design

### 3.1 Entity-Relationship (ER) Description
-  have a  relationship with  (a vehicle can visit multiple times over time, but only has at most one active ticket).
-  have a **1-to relationship with  (a parking slot hosts multiple parking sessions over time).
- maintain a lookup for billing parameters per vehicle class.

### 3.2 Schema Architecture

#### Table: `vehicles`
- `license_plate` (VARCHAR(15), : Vehicle registration number.
- `vehicle_type` (VARCHAR(20): Type classification (`MOTORCYCLE`, `COMPACT`, `LARGE`).
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP).

#### Table: `parking_slots`
- `slot_id` (VARCHAR(10), : Unique identifier (e.g., `A-101`).
- `vehicle_type` (VARCHAR(20), **NOT NULL**): Vehicle class restriction.
- `is_occupied` (BOOLEAN, DEFAULT FALSE): Operational state flag.

#### Table: `parking_tickets`
- `ticket_id` (VARCHAR(36), : Unique ticket UUID.
`entry_timestamp` (TIMESTAMP, 
- `exit_timestamp` (TIMESTAMP, NULLABLE).
- `total_fee` (DECIMAL(10, 2), NULLABLE).
- `status` (VARCHAR(15), : `ACTIVE` or `COMPLETED`