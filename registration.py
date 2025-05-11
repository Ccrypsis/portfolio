# Anthony Robbins, CIS 345, Final Project, Online

import json
import os

JSON_FILE = "registrations.json"

class Registration:
    def __init__(self, name: str, email: str, class_name: str, time: str, duration: float, fee: int):
        self.name = name
        self.email = email
        self.class_name = class_name
        self.time = time
        self.duration = float(duration)
        self.fee = int(fee)

    def summary(self):
        return f"{self.name} | {self.email} | {self.class_name} at {self.time} - {self.duration:.2f}hrs - ${self.fee}"

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "class": self.class_name,
            "time": self.time,
            "duration": self.duration,
            "fee": self.fee
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"], data["class"], data["time"], data.get("duration", 1.5), data.get("fee", 10))

def load_registrations():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, "r") as f:
        return [Registration.from_dict(entry) for entry in json.load(f)]

def save_registrations(registrations):
    with open(JSON_FILE, "w") as f:
        json.dump([r.to_dict() for r in registrations], f, indent=2)

def register_customer(name, email, class_name, time, duration=1.0, fee=10):
    registrations = load_registrations()
    for r in registrations:
        if r.name.casefold() == name.casefold() and \
           r.class_name.casefold() == class_name.casefold() and \
           r.time.casefold() == time.casefold():
            return False  # Duplicate
    registrations.append(Registration(name, email, class_name, time, duration, fee))
    save_registrations(registrations)
    return True

def cancel_registration(name, email, class_name, time):
    name = name.strip().casefold()
    email = email.strip().casefold()
    class_name = class_name.strip().casefold()
    time = time.strip()

    registrations = load_registrations()
    updated = []
    found = False

    for r in registrations:
        if (
            r.name.strip().casefold() == name and
            r.email.strip().casefold() == email and
            r.class_name.strip().casefold() == class_name and
            r.time.strip() == time
        ):
            found = True
            continue  # skip this one to "delete" it
        updated.append(r)

    if found:
        save_registrations(updated)
        return True
    else:
        return False

def display_grouped():
    registrations = load_registrations()
    grouped = {}
    for r in registrations:
        key = f"{r.class_name.title()} at {r.time}"
        grouped.setdefault(key, []).append(r)
    output = []
    for key in sorted(grouped):
        output.append(f"=== {key} ===")
        for r in sorted(grouped[key], key=lambda x: x.name.lower()):
            output.append(r.summary())
    return output


