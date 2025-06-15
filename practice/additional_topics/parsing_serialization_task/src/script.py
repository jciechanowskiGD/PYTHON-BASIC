import json
import os
from lxml import etree


def read_day(filepath: str) -> dict:
    with open(filepath, "r") as file:
        day_data = json.load(file)
        return day_data


def calculate_stats_for_day(day_data: dict) -> dict:
    stats = {
        "mean_temp": 0,
        "mean_wind_speed": 0,
        "min_temp": float("+inf"),
        "min_wind_speed": float("+inf"),
        "max_temp": float("-inf"),
        "max_wind_speed": float("-inf"),
    }

    hours = len(day_data["hourly"])

    for hour in day_data["hourly"]:
        temp = hour["temp"]
        wind_speed = hour["wind_speed"]

        stats["mean_temp"] += temp / hours
        stats["mean_wind_speed"] += wind_speed / hours

        if stats["min_temp"] > temp:
            stats["min_temp"] = temp

        if stats["min_wind_speed"] > wind_speed:
            stats["min_wind_speed"] = wind_speed

        if stats["max_temp"] < temp:
            stats["max_temp"] = temp

        if stats["max_wind_speed"] < wind_speed:
            stats["max_wind_speed"] = wind_speed

    stats["mean_temp"] = round(stats["mean_temp"], 2)
    stats["mean_wind_speed"] = round(stats["mean_wind_speed"], 2)

    return stats


def calculate_summary(cities_stats: dict) -> dict:
    summary = {
        "mean_temp": 0,
        "mean_wind_speed": 0,
        "coldest_place": None,
        "warmest_place": None,
        "windiest_place": None,
    }

    cities_amount = len(cities_stats)
    coldest = [float("+inf"), None]
    warmest = [float("-inf"), None]
    windiest = [float("-inf"), None]

    for city in cities_stats:
        summary["mean_temp"] += cities_stats[city]["mean_temp"] / cities_amount
        summary["mean_wind_speed"] += (
            cities_stats[city]["mean_wind_speed"] / cities_amount
        )

        if coldest[0] > cities_stats[city]["mean_temp"]:
            coldest[0] = cities_stats[city]["mean_temp"]
            coldest[1] = city

        if warmest[0] < cities_stats[city]["mean_temp"]:
            warmest[0] = cities_stats[city]["mean_temp"]
            warmest[1] = city

        if windiest[0] < cities_stats[city]["mean_wind_speed"]:
            windiest[0] = cities_stats[city]["mean_wind_speed"]
            windiest[1] = city

    summary["coldest_place"] = coldest[1]
    summary["warmest_place"] = warmest[1]
    summary["windiest_place"] = windiest[1]

    summary["mean_temp"] = round(summary["mean_temp"], 2)
    summary["mean_wind_speed"] = round(summary["mean_wind_speed"], 2)

    return summary


def calculate_for_all_cities_one_day(folder_path: str) -> dict:
    cities_stats = {}
    cities = os.listdir(folder_path)

    for city in cities:
        filepath = f"{folder_path}/{city}/2021_09_25.json"
        day_data = read_day(filepath)
        cities_stats[city] = calculate_stats_for_day(day_data)

    final_stats = {}

    final_stats["summary"] = calculate_summary(cities_stats)
    final_stats |= cities_stats

    return final_stats


def change_to_right_format(final_stats: dict) -> etree.ElementTree:
    weather = etree.Element("weather", country="Spain", date="2021-09-25")

    summary_d = final_stats["summary"]
    summary = etree.SubElement(
        weather,
        "summary",
        mean_temp=str(summary_d["mean_temp"]),
        mean_wind_speed=str(summary_d["mean_wind_speed"]),
        coldest_place=str(summary_d["coldest_place"]),
        warmest_place=str(summary_d["warmest_place"]),
        windiest_place=str(summary_d["windiest_place"]),
    )

    final_stats["Santiago_de_Compostela"] = final_stats["Santiago de Compostela"]
    del final_stats["Santiago de Compostela"]

    final_stats["Santa_Cruz_de_Tenerife"] = final_stats["Santa Cruz de Tenerife"]
    del final_stats["Santa Cruz de Tenerife"]

    cities = etree.Element("cities")
    for city in final_stats:
        if city == "summary":
            continue
        etree.SubElement(
            cities,
            city,
            mean_temp=str(final_stats[city]["mean_temp"]),
            mean_wind_speed=str(final_stats[city]["mean_wind_speed"]),
            min_temp=str(final_stats[city]["min_temp"]),
            min_wind_speed=str(final_stats[city]["min_wind_speed"]),
            max_temp=str(final_stats[city]["max_temp"]),
            max_wind_speed=str(final_stats[city]["max_wind_speed"]),
        )
    weather.append(cities)
    return weather

def save_to_file(xml_element) -> None:
    tree = etree.ElementTree(xml_element)
    tree.write('result.xml',pretty_print=True, encoding='utf-8')


if __name__ == "__main__":
    final_stats = calculate_for_all_cities_one_day("./source_data")
    result = change_to_right_format(final_stats)
    print(etree.tostring(result, pretty_print=True).decode(), end = '')
    save_to_file(result)