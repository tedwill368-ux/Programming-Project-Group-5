"""CSV storage helpers for the Airline Management System."""
import csv
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

PASSENGER_FILE = os.path.join(DATA_DIR, "passengers.csv")
FLIGHT_FILE = os.path.join(DATA_DIR, "flights.csv")
BOOKING_FILE = os.path.join(DATA_DIR, "bookings.csv")

HEADERS = {
    PASSENGER_FILE: ["passenger_id", "full_name", "phone", "email"],
    FLIGHT_FILE: [
        "flight_id", "origin", "destination", "travel_date", "departure_time",
        "price", "seat_capacity", "available_seats"
    ],
    BOOKING_FILE: [
        "booking_reference", "passenger_id", "flight_id", "booking_date",
        "total_price", "status"
    ],
}


def ensure_data_files():
    """Create the data directory and CSV files with headers when absent."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for path, headers in HEADERS.items():
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            with open(path, "w", newline="", encoding="utf-8") as file:
                csv.writer(file).writerow(headers)


def load_records(path):
    ensure_data_files()
    try:
        with open(path, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except (OSError, csv.Error) as error:
        print(f"Could not read {os.path.basename(path)}: {error}")
        return []


def save_records(path, records):
    ensure_data_files()
    headers = HEADERS[path]
    try:
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(records)
        return True
    except (OSError, csv.Error) as error:
        print(f"Could not save {os.path.basename(path)}: {error}")
        return False


def next_id(records, field, prefix):
    """Generate the next sequential ID, e.g. P001 or F001."""
    highest = 0
    for record in records:
        value = record.get(field, "")
        digits = "".join(character for character in value if character.isdigit())
        if digits:
            highest = max(highest, int(digits))
    return f"{prefix}{highest + 1:03d}"
