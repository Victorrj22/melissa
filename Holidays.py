import requests
from typing import List, Optional

token: str = "17321|H0sCrqpfrb5QNeRXA5mQDxD243eyaqIP"


class Holiday:
    #Faz o mapeamento do retorno da API
    def __init__(self, date: str, name: str, holiday_type: str, level: str, law: Optional[str] = None):
        self.date = date
        self.name = name
        self.holiday_type = holiday_type
        self.level = level
        self.law = law


    def __repr__(self):
        return (f"Holiday(Date: {self.date}, Name: {self.name}, Type: {self.holiday_type}, "
                f"Level: {self.level}, Law: {self.law})")

def get_holidays(state: str, year: int, api_token: str) -> List[Holiday]:
    endpoint = f"https://api.invertexto.com/v1/holidays/{year}?token={api_token}&state={state}"
    try:
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        holidays_data = response.json()
        mapped_holidays = [
            Holiday(
                date=holiday["date"],
                name=holiday["name"],
                holiday_type=holiday["type"],
                level=holiday["level"],
                law=holiday.get("law")
            )
            for holiday in holidays_data
        ]
        return mapped_holidays
    except requests.exceptions.RequestException as e:
        print(f"Algo de errado não deu certo: {e}")
        return []