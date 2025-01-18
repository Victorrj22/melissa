import requests  # type: ignore
import os
from typing import List
from dotenv import load_dotenv
from ..Holidays.Holiday import Holiday  # type: ignore

class HolidayService:
    def __init__(self, from_online_source: bool = False):
        self.__from_online_source = from_online_source

        load_dotenv()
        api_token = os.getenv("INVERTETEXTO_API_TOKEN")
        if not api_token:
            raise ValueError("INVERTETEXTO_API_TOKEN não encontrado no arquivo .env")

        self.__api_token: str = api_token


    def get_holidays(self, state: str, year: int, month: int) -> List[Holiday]:
        if self.__from_online_source:
            return self.__fetch_from_external_api(state, year, month)
        return self.__fetch_from_local_data(state, year, month)


    def __fetch_from_external_api(self, state: str, year: int, month: int) -> List[Holiday]:
        endpoint = f"https://api.invertexto.com/v1/holidays/{year}?token={self.__api_token}&state={state}"

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
