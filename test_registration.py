# Anthony Robbins, CIS 345, Final Project, Online

import unittest
from registration import Registration

class TestRegistration(unittest.TestCase):

    def test_summary(self):
        print("This checks that the method returns the right string format")
        reg = Registration("John Doe", "john@example.com", "Yoga", "9:00 AM", 2.5, 10)
        self.assertEqual(reg.summary(), "John Doe | john@example.com | Yoga at 9:00 AM - 2.50hrs - $10")

    def test_to_dict(self):
        print("This verifies that our object can be converted into a dictionary correctly")
        reg = Registration("Alice", "alice@example.com", "Spin", "1:00 PM", 1.0, 10)
        expected = {
            "name": "Alice",
            "email": "alice@example.com",
            "class": "Spin",
            "time": "1:00 PM",
            "duration": 1.0,
            "fee": 10
        }
        self.assertEqual(reg.to_dict(), expected)

    def test_from_dict(self):
        print("This confirms that our class can be created from a dictionary")
        data = {
            "name": "Bob",
            "email": "bob@example.com",
            "class": "Zumba",
            "time": "3:00 PM",
            "duration": 1.0,
            "fee": 10
        }
        reg = Registration.from_dict(data)
        self.assertEqual(reg.name, "Bob")
        self.assertEqual(reg.email, "bob@example.com")
        self.assertEqual(reg.class_name, "Zumba")
        self.assertEqual(reg.time, "3:00 PM")
        self.assertEqual(reg.duration, 1.0)
        self.assertEqual(reg.fee, 10)

if __name__ == "__main__":
    unittest.main()
