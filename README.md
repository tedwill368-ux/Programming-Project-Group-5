# Airline Management System — INFO 301

A basic Python console prototype for managing fictional airline passengers, flight schedules, and simulated ticket bookings. It does not connect to a real airline reservation network and does not process real payments or issue real tickets.

## Requirements

- Python 3.9 or later
- No external Python packages are required.

## Run the program

1. Extract the project ZIP file.
2. Open a terminal or command prompt in the `airline_management_system` folder.
3. Run:

```bash
python main.py
```

On some Windows installations, use `py main.py`.

The application creates the `data` folder and CSV files with headers if they do not already exist.

## Main features

1. Passenger registration, listing, searching, and updating.
2. Add, view, update, and remove flight records.
3. Search flights by origin, destination, and travel date.
4. Book a passenger on a flight and generate a booking reference.
5. View a booking and cancel a confirmed booking.
6. Restore one available seat when a booking is cancelled.
7. Display confirmed passengers for a flight.
8. View bookings by status.

## CSV data files

- `data/passengers.csv`: passenger ID, name, phone, email.
- `data/flights.csv`: flight ID, route, date, time, ticket price, seat capacity, available seats.
- `data/bookings.csv`: booking reference, passenger ID, flight ID, booking date, total price, status.

The included CSV files contain fictional demonstration records. Keep the three CSV files in the `data` folder. The program saves changes to these files, so records remain after the program closes.

## Date and time formats

- Date: `YYYY-MM-DD`
- Time: `HH:MM` using the 24-hour clock.

## Important rules and limitations

- Use fictional passengers and flights only.
- Passenger and flight IDs must exist before a booking can be created.
- A booking cannot be made if the flight has no available seats.
- This basic version books one seat for one passenger per booking.
- Cancelling a confirmed booking restores one seat.
- Prices are simulated; no real payment is taken.
- No GUI, SQL database, external API, or real airline network is used.

## Suggested demonstration

1. View the passenger list and flight schedule.
2. Search for a flight using its origin, destination, and date.
3. Book a passenger on that flight.
4. View the booking using its generated reference.
5. Display the passenger list for that flight.
6. Cancel the booking and show that the available seat count increases.
7. Exit and run the program again to demonstrate CSV persistence.

## Test checklist

- [ ] Register a passenger and confirm that the passenger ID is generated.
- [ ] Search for an existing passenger and a non-existing passenger.
- [ ] Add a flight with a valid date and time.
- [ ] Search for a matching flight.
- [ ] Try searching with an invalid date.
- [ ] Create a booking using existing passenger and flight IDs.
- [ ] Try booking with a non-existing passenger ID.
- [ ] Try booking with a non-existing flight ID.
- [ ] Try booking a flight with zero available seats.
- [ ] Cancel a confirmed booking and confirm that one seat is restored.
- [ ] Try cancelling the same booking again.
- [ ] Close and reopen the program to confirm that saved records remain.

## Project structure

```text
airline_management_system/
├── main.py
├── storage.py
├── passengers.py
├── flights.py
├── bookings.py
├── README.md
├── tests/
│   └── test_system.py
└── data/
    ├── passengers.csv
    ├── flights.csv
    └── bookings.csv
```
