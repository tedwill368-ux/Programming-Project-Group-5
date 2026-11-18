"""INFO 301 - Airline Management System (console-based Python project)."""
from storage import ensure_data_files
from passengers import passenger_menu
from flights import flight_menu, search_flights
from bookings import booking_menu, passenger_list_for_flight


def main():
    ensure_data_files()
    print("=" * 55)
    print("          AIRLINE MANAGEMENT SYSTEM")
    print("        INFO 301 - SEMESTER 2, 2026")
    print("=" * 55)

    while True:
        print("\nMAIN MENU")
        print("1. Passenger Management")
        print("2. Flight Management")
        print("3. Search Flights")
        print("4. Book Ticket")
        print("5. View/Cancel Booking")
        print("6. Flight Passenger List")
        print("7. Exit")
        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            passenger_menu()
        elif choice == "2":
            flight_menu()
        elif choice == "3":
            search_flights()
        elif choice == "4":
            from bookings import create_booking
            create_booking()
        elif choice == "5":
            booking_menu()
        elif choice == "6":
            passenger_list_for_flight()
        elif choice == "7":
            print("Data is saved in the CSV files. Program closed.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped. Previously saved data remains in the CSV files.")
