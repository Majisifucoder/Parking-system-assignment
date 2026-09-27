create table  vehicles (
    license_plate VARCHAR(15) PRIMARY KEY,
    vehicle_type VARCHAR(20) NOT NULL CHECK (vehicle_type IN ('MOTORCYCLE', 'COMPACT', 'LARGE')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table  parking_slots (
    slot_id VARCHAR(10) PRIMARY KEY,
    vehicle_type VARCHAR(20) NOT NULL CHECK (vehicle_type IN ('MOTORCYCLE', 'COMPACT', 'LARGE')),
    is_occupied BOOLEAN DEFAULT FALSE
);

create table  parking_tickets (
    ticket_id VARCHAR(36) PRIMARY KEY,
    license_plate VARCHAR(15) NOT NULL,
    slot_id VARCHAR(10) NOT NULL,
    entry_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exit_timestamp TIMESTAMP NULL,
    total_fee DECIMAL(10, 2) NULL,
    status VARCHAR(15) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'COMPLETED')),
    FOREIGN KEY (license_plate) REFERENCES vehicles(license_plate) ON DELETE RESTRICT,
    FOREIGN KEY (slot_id) REFERENCES parking_slots(slot_id) ON DELETE RESTRICT
);

-- Indexing for optimized exit query execution
create idx_slots_type_occupiedndexX idx_tickets_active_plate ON parking_tickets (license_plate) WHERE status = 'ACTIVE';
create idx_slots_type_occupiedndexX idx_slots_type_occupied ON parking_slots (vehicle_type, is_occupied);