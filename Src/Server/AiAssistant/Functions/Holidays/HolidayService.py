import requests
from typing import List

from Src.Server.AiAssistant.Functions.Holidays.Holiday import Holiday


class HolidayService:
    def __init__(self, from_online_source: bool = False):
        self.__from_online_source = from_online_source

    def get_holidays(self, state: str, year: int, month: int) -> List[Holiday]:
        if self.__from_online_source:
            return self.__fetch_from_external_api(state, year, month)

        return self.__fetch_from_local_data(state, year, month)


    @staticmethod
    def __fetch_from_external_api(state: str, year: int, month: int) -> List[Holiday]:
        api_token = "17321|H0sCrqpfrb5QNeRXA5mQDxD243eyaqIP"
        endpoint = f"https://api.invertexto.com/v1/holidays/{year}?token={api_token}&state={state}"

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
            for holiday in holidays_data if int(holiday["date"].split("-")[1]) == month
        ]

        return mapped_holidays


    @staticmethod
    def __fetch_from_local_data(state: str, year: int, month: int) -> List[Holiday]:
        raise NotImplementedError("Este método ainda não foi implementado")
