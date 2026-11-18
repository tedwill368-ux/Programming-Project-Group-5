"""Ticket booking, cancellation, and booking reports."""
from datetime import date
from storage import (
    PASSENGER_FILE, FLIGHT_FILE, BOOKING_FILE,
    load_records, save_records, next_id
)


def create_booking():
    passengers = load_records(PASSENGER_FILE)
    flights = load_records(FLIGHT_FILE)
    bookings = load_records(BOOKING_FILE)

    print("\nBOOK TICKET")
    passenger_id = input("Passenger ID: ").strip()
    passenger = next((p for p in passengers if p["passenger_id"].lower() == passenger_id.lower()), None)
    if not passenger:
        print("Passenger ID does not exist. Register the passenger first.")
        return

    flight_id = input("Flight ID: ").strip()
    flight = next((f for f in flights if f["flight_id"].lower() == flight_id.lower()), None)
    if not flight:
        print("Flight ID does not exist.")
        return

    available = int(flight["available_seats"])
    if available < 1:
        print("This flight has no available seats.")
        return

    # One passenger occupies one seat in this basic prototype.
    total_price = float(flight["price"])
    reference = next_id(bookings, "booking_reference", "B")
    bookings.append({
        "booking_reference": reference,
        "passenger_id": passenger["passenger_id"],
        "flight_id": flight["flight_id"],
        "booking_date": date.today().isoformat(),
        "total_price": f"{total_price:.2f}",
        "status": "CONFIRMED",
    })
    flight["available_seats"] = str(available - 1)

    # Save flight and booking records; restore in-memory seat count if either save fails.
    if not save_records(FLIGHT_FILE, flights):
        return
    if not save_records(BOOKING_FILE, bookings):
        flight["available_seats"] = str(available)
        save_records(FLIGHT_FILE, flights)
        return
    print(f"Booking confirmed. Reference: {reference}")
    print(f"Passenger: {passenger['full_name']}")
    print(f"Flight: {flight['flight_id']} - {flight['origin']} to {flight['destination']}")
    print(f"Total ticket price: ${total_price:.2f}")


def view_booking():
    reference = input("Booking reference: ").strip()
    bookings = load_records(BOOKING_FILE)
    booking = next((b for b in bookings if b["booking_reference"].lower() == reference.lower()), None)
    if not booking:
        print("Booking not found.")
        return
    passengers = load_records(PASSENGER_FILE)
    flights = load_records(FLIGHT_FILE)
    passenger = next((p for p in passengers if p["passenger_id"] == booking["passenger_id"]), None)
    flight = next((f for f in flights if f["flight_id"] == booking["flight_id"]), None)
    print("\nBOOKING DETAILS")
    print(f"Reference: {booking['booking_reference']}")
    print(f"Passenger: {passenger['full_name'] if passenger else booking['passenger_id']}")
    if flight:
        print(f"Flight: {flight['flight_id']} | {flight['origin']} to {flight['destination']}")
        print(f"Travel: {flight['travel_date']} at {flight['departure_time']}")
    print(f"Total price: ${float(booking['total_price']):.2f}")
    print(f"Status: {booking['status']}")


def cancel_booking():
    reference = input("Booking reference to cancel: ").strip()
    bookings = load_records(BOOKING_FILE)
    booking = next((b for b in bookings if b["booking_reference"].lower() == reference.lower()), None)
    if not booking:
        print("Booking not found.")
        return
    if booking["status"] != "CONFIRMED":
        print("Only confirmed bookings can be cancelled.")
        return
    flights = load_records(FLIGHT_FILE)
    flight = next((f for f in flights if f["flight_id"] == booking["flight_id"]), None)
    if not flight:
        print("The related flight record is missing. Cancellation cannot safely restore a seat.")
        return
    if int(flight["available_seats"]) < int(flight["seat_capacity"]):
        flight["available_seats"] = str(int(flight["available_seats"]) + 1)
    booking["status"] = "CANCELLED"
    if not save_records(FLIGHT_FILE, flights):
        return
    if not save_records(BOOKING_FILE, bookings):
        flight["available_seats"] = str(int(flight["available_seats"]) - 1)
        save_records(FLIGHT_FILE, flights)
        return
    print(f"Booking {reference} cancelled. One seat has been restored.")


def passenger_list_for_flight():
    flight_id = input("Flight ID: ").strip()
    flights = load_records(FLIGHT_FILE)
    flight = next((f for f in flights if f["flight_id"].lower() == flight_id.lower()), None)
    if not flight:
        print("Flight not found.")
        return
    passengers = load_records(PASSENGER_FILE)
    bookings = load_records(BOOKING_FILE)
    confirmed = [b for b in bookings if b["flight_id"] == flight["flight_id"] and b["status"] == "CONFIRMED"]
    print(f"\nPASSENGERS ON FLIGHT {flight['flight_id']}")
    print(f"{flight['origin']} to {flight['destination']} | {flight['travel_date']}")
    if not confirmed:
        print("No confirmed passengers.")
        return
    for booking in confirmed:
        passenger = next((p for p in passengers if p["passenger_id"] == booking["passenger_id"]), None)
        if passenger:
            print(f"{passenger['passenger_id']} | {passenger['full_name']} | {passenger['phone']}")


def bookings_by_status():
    status = input("Enter status (CONFIRMED or CANCELLED): ").strip().upper()
    if status not in ("CONFIRMED", "CANCELLED"):
        print("Enter CONFIRMED or CANCELLED.")
        return
    bookings = [b for b in load_records(BOOKING_FILE) if b["status"] == status]
    if not bookings:
        print(f"No {status.lower()} bookings found.")
        return
    for b in bookings:
        print(f"{b['booking_reference']} | Passenger: {b['passenger_id']} | Flight: {b['flight_id']} | ${float(b['total_price']):.2f}")


def booking_menu():
    while True:
        print("\n--- BOOKING MANAGEMENT ---")
        print("1. Book ticket")
        print("2. View booking")
        print("3. Cancel booking")
        print("4. View bookings by status")
        print("5. Return to main menu")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            create_booking()
        elif choice == "2":
            view_booking()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            bookings_by_status()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Enter 1–5.")
