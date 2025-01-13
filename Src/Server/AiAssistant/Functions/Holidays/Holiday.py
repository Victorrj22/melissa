from typing import Optional

class Holiday:
    def __init__(self, date: str, name: str, holiday_type: str, level: str, law: Optional[str] = None):
        self.date = date
        self.name = name
        self.holiday_type = holiday_type
        self.level = level
        self.law = law


    def __repr__(self):
        return (f"Holiday(Date: {self.date}, Name: {self.name}, Type: {self.holiday_type}, "
                f"Level: {self.level}, Law: {self.law})")