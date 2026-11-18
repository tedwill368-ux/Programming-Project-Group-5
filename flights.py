"""Flight schedule management and flight search."""
from datetime import datetime
from storage import FLIGHT_FILE, load_records, save_records, next_id


def list_flights():
    flights = load_records(FLIGHT_FILE)
    if not flights:
        print("No flights found.")
        return
    print("\nFLIGHT SCHEDULE")
    print("-" * 105)
    for f in flights:
        print(
            f"{f['flight_id']:<7} {f['origin']:<16} {f['destination']:<16} "
            f"{f['travel_date']:<12} {f['departure_time']:<7} "
            f"${float(f['price']):>8.2f}  Seats: {f['available_seats']}/{f['seat_capacity']}"
        )
    print("-" * 105)


def add_flight():
    flights = load_records(FLIGHT_FILE)
    print("\nADD FLIGHT")
    origin = input("Origin: ").strip()
    destination = input("Destination: ").strip()
    travel_date = input("Travel date (YYYY-MM-DD): ").strip()
    departure_time = input("Departure time (HH:MM): ").strip()
    try:
        datetime.strptime(travel_date, "%Y-%m-%d")
        datetime.strptime(departure_time, "%H:%M")
        price = float(input("Ticket price: ").strip())
        capacity = int(input("Seat capacity: ").strip())
        if price < 0 or capacity < 1:
            raise ValueError
    except ValueError:
        print("Invalid date, time, price, or capacity. No flight was added.")
        return
    if not origin or not destination or origin.lower() == destination.lower():
        print("Enter valid, different origin and destination cities.")
        return
    flight_id = next_id(flights, "flight_id", "F")
    flights.append({
        "flight_id": flight_id,
        "origin": origin,
        "destination": destination,
        "travel_date": travel_date,
        "departure_time": departure_time,
        "price": f"{price:.2f}",
        "seat_capacity": str(capacity),
        "available_seats": str(capacity),
    })
    if save_records(FLIGHT_FILE, flights):
        print(f"Flight added successfully. Flight ID: {flight_id}")


def find_flight(flight_id):
    return next(
        (f for f in load_records(FLIGHT_FILE)
         if f["flight_id"].lower() == flight_id.lower()),
        None
    )


def search_flights():
    print("\nSEARCH FLIGHTS")
    origin = input("Origin: ").strip().lower()
    destination = input("Destination: ").strip().lower()
    travel_date = input("Travel date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(travel_date, "%Y-%m-%d")
    except ValueError:
        print("Date must use YYYY-MM-DD.")
        return
    matches = [
        f for f in load_records(FLIGHT_FILE)
        if f["origin"].lower() == origin
        and f["destination"].lower() == destination
        and f["travel_date"] == travel_date
        and int(f["available_seats"]) > 0
    ]
    if not matches:
        print("No available flights match those details.")
        return
    for f in matches:
        print(
            f"{f['flight_id']} | {f['origin']} to {f['destination']} | "
            f"{f['travel_date']} {f['departure_time']} | "
            f"${float(f['price']):.2f} | {f['available_seats']} seat(s) available"
        )


def update_flight():
    flights = load_records(FLIGHT_FILE)
    flight_id = input("Flight ID to update: ").strip()
    flight = next((f for f in flights if f["flight_id"].lower() == flight_id.lower()), None)
    if not flight:
        print("Flight not found.")
        return
    print("Press Enter to keep the current value.")
    origin = input(f"Origin [{flight['origin']}]: ").strip()
    destination = input(f"Destination [{flight['destination']}]: ").strip()
    date = input(f"Date [{flight['travel_date']}]: ").strip()
    time = input(f"Time [{flight['departure_time']}]: ").strip()
    price_text = input(f"Price [{flight['price']}]: ").strip()
    capacity_text = input(f"Seat capacity [{flight['seat_capacity']}]: ").strip()
    try:
        if date:
            datetime.strptime(date, "%Y-%m-%d")
            flight["travel_date"] = date
        if time:
            datetime.strptime(time, "%H:%M")
            flight["departure_time"] = time
        if price_text:
            price = float(price_text)
            if price < 0:
                raise ValueError
            flight["price"] = f"{price:.2f}"
        if capacity_text:
            new_capacity = int(capacity_text)
            booked = int(flight["seat_capacity"]) - int(flight["available_seats"])
            if new_capacity < booked or new_capacity < 1:
                print(f"Capacity cannot be less than the {booked} already-booked seat(s).")
                return
            flight["seat_capacity"] = str(new_capacity)
            flight["available_seats"] = str(new_capacity - booked)
    except ValueError:
        print("Invalid value. Flight was not updated.")
        return
    if origin:
        flight["origin"] = origin
    if destination:
        flight["destination"] = destination
    if flight["origin"].lower() == flight["destination"].lower():
        print("Origin and destination must be different.")
        return
    if save_records(FLIGHT_FILE, flights):
        print("Flight updated successfully.")


def remove_flight():
    flights = load_records(FLIGHT_FILE)
    flight_id = input("Flight ID to remove: ").strip()
    flight = next((f for f in flights if f["flight_id"].lower() == flight_id.lower()), None)
    if not flight:
        print("Flight not found.")
        return
    from storage import BOOKING_FILE
    bookings = load_records(BOOKING_FILE)
    if any(b["flight_id"] == flight_id and b["status"] == "CONFIRMED" for b in bookings):
        print("Cannot remove a flight that has confirmed bookings.")
        return
    flights.remove(flight)
    if save_records(FLIGHT_FILE, flights):
        print("Flight removed successfully.")


def flight_menu():
    while True:
        print("\n--- FLIGHT MANAGEMENT ---")
        print("1. Add flight")
        print("2. View all flights")
        print("3. Update flight")
        print("4. Remove flight")
        print("5. Return to main menu")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_flight()
        elif choice == "2":
            list_flights()
        elif choice == "3":
            update_flight()
        elif choice == "4":
            remove_flight()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Enter 1–5.")
