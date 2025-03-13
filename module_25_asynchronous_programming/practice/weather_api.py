import asyncio
from pathlib import Path
from datetime import datetime
import time

from aiohttp import ClientSession
import aiofiles


KELVIN = 273.15
OUT_PATH = Path(__file__).parent / "weather"
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()
FILE_NAME = "report_on_weather.txt"


def convert_K_to_C(value: float) -> float:
    """
    Конвертер градусов из Кельвин в Цельсия
    """
    celsius = value - KELVIN
    return round(celsius, 1)


async def write_to_file(report: str) -> None:
    """
    Запись отчета по погоде в файл `report_on_weather.txt`
    """
    file_name = "{}/{}".format(OUT_PATH, FILE_NAME)
    data = datetime.today().strftime('%Y-%m-%d %H:%M')
    async with aiofiles.open(file_name, "a") as file:
        await file.write(f"{data} == {report}\n")


def read_report():
    """
    Чтение файла "отчет по пагоде"
    """
    with open(OUT_PATH / FILE_NAME, "r") as file:
        for f in file.readlines():
            print(f)


async def get_weather(city):
    async with ClientSession() as session:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "APPID": "2a4ff86f9aaa70041ec8e82db64abf56"}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            convert = weather_json["main"]["temp"]
            report_weather = f'{city}: {weather_json["weather"][0]["main"]} | {convert_K_to_C(convert)} °C | {convert} °K'
            await write_to_file(report_weather)
            # print(f'{city}: {weather_json["weather"][0]["main"]} | {convert_K_to_C(convert)} °C | {convert} °K')


async def main(cities_):
    tasks = [asyncio.create_task(get_weather(city)) for city in cities_]

    # for task in tasks:
    #     await task
    
    return await asyncio.gather(*tasks)


cities = [
    "Moscow",
    "St. Petersburg",
    "Rostov-on-Don",
    "Kaliningrad",
    "Vladivostok",
    "Minsk",
    "Beijing",
    "Delhi",
    "Istanbul",
    "Tokyo",
    "London",
    "New York",
    "Novosibirsk",
]

start = time.time()
asyncio.run(main(cities))
print(f"\nОтчет с погодой по городам - Готов! Время сбора данных - {time.time() - start}s\n")

read_report()
