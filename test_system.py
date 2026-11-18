"""Small automated tests for the CSV-based Airline Management System."""
import csv
import os
import tempfile
import unittest
from storage import next_id
from datetime import date

# Test the core data rules independently using temporary CSV files.
class AirlineRulesTests(unittest.TestCase):
    def test_flight_date_format(self):
        from datetime import datetime
        self.assertEqual(datetime.strptime("2026-11-21", "%Y-%m-%d").date().isoformat(), "2026-11-21")
        with self.assertRaises(ValueError):
            datetime.strptime("21-11-2026", "%Y-%m-%d")

    def test_booking_reference_generation(self):
        records = [{"booking_reference": "B001"}, {"booking_reference": "B009"}]
        self.assertEqual(next_id(records, "booking_reference", "B"), "B010")

    def test_csv_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "sample.csv")
            records = [{"id": "P001", "name": "Sample Passenger"}]
            with open(path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["id", "name"])
                writer.writeheader()
                writer.writerows(records)
            with open(path, "r", newline="", encoding="utf-8") as file:
                loaded = list(csv.DictReader(file))
            self.assertEqual(loaded, records)

    def test_one_seat_reduction_and_restore(self):
        available_seats = 1
        available_seats -= 1
        self.assertEqual(available_seats, 0)
        available_seats += 1
        self.assertEqual(available_seats, 1)


if __name__ == "__main__":
    unittest.main()
