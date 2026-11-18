"""Passenger registration and record management."""
from storage import PASSENGER_FILE, load_records, save_records, next_id


def list_passengers():
    passengers = load_records(PASSENGER_FILE)
    if not passengers:
        print("No passenger records found.")
        return
    print("\nPASSENGER RECORDS")
    print("-" * 75)
    for p in passengers:
        print(f"{p['passenger_id']:<8} {p['full_name']:<25} {p['phone']:<18} {p['email']}")
    print("-" * 75)


def register_passenger():
    passengers = load_records(PASSENGER_FILE)
    print("\nREGISTER PASSENGER")
    name = input("Full name: ").strip()
    phone = input("Phone number: ").strip()
    email = input("Email address: ").strip()
    if not name or not phone or not email:
        print("All fields are required.")
        return
    if any(p["email"].lower() == email.lower() for p in passengers):
        print("A passenger with that email already exists.")
        return
    passenger_id = next_id(passengers, "passenger_id", "P")
    passengers.append({
        "passenger_id": passenger_id,
        "full_name": name,
        "phone": phone,
        "email": email,
    })
    if save_records(PASSENGER_FILE, passengers):
        print(f"Passenger registered successfully. Passenger ID: {passenger_id}")


def find_passenger(passenger_id):
    return next(
        (p for p in load_records(PASSENGER_FILE)
         if p["passenger_id"].lower() == passenger_id.lower()),
        None
    )


def search_passenger():
    term = input("Enter passenger ID, name, or email: ").strip().lower()
    matches = [
        p for p in load_records(PASSENGER_FILE)
        if term in p["passenger_id"].lower()
        or term in p["full_name"].lower()
        or term in p["email"].lower()
    ]
    if not matches:
        print("No matching passenger found.")
        return
    for p in matches:
        print(f"{p['passenger_id']} | {p['full_name']} | {p['phone']} | {p['email']}")


def update_passenger():
    passengers = load_records(PASSENGER_FILE)
    passenger_id = input("Passenger ID to update: ").strip()
    passenger = next((p for p in passengers if p["passenger_id"].lower() == passenger_id.lower()), None)
    if not passenger:
        print("Passenger not found.")
        return
    print("Press Enter to keep the current value.")
    name = input(f"Full name [{passenger['full_name']}]: ").strip()
    phone = input(f"Phone [{passenger['phone']}]: ").strip()
    email = input(f"Email [{passenger['email']}]: ").strip()
    if name:
        passenger["full_name"] = name
    if phone:
        passenger["phone"] = phone
    if email:
        if any(p is not passenger and p["email"].lower() == email.lower() for p in passengers):
            print("That email is already assigned to another passenger.")
            return
        passenger["email"] = email
    if save_records(PASSENGER_FILE, passengers):
        print("Passenger updated successfully.")


def passenger_menu():
    while True:
        print("\n--- PASSENGER MANAGEMENT ---")
        print("1. Register passenger")
        print("2. View all passengers")
        print("3. Search passenger")
        print("4. Update passenger")
        print("5. Return to main menu")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            register_passenger()
        elif choice == "2":
            list_passengers()
        elif choice == "3":
            search_passenger()
        elif choice == "4":
            update_passenger()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Enter 1–5.")
