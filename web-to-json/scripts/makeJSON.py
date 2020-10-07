import csv
import json
import re
import sys
from pathlib import Path

NON_CITY_KEYS = set(["variety", "commodity", "unit", "weight", "code", "average", "max", "min", "stdev", "date"])
PATH_TO_JSON_FOLDER = Path("../json/")

# def parse_args(args):
#     if len(args) != 2:
#         print("Run file with `python makeJSON.py <path-to-csv>'.\nExiting...")
#         exit()
#     else:
#         csv_name = args[1] if args[1][-4:] == ".csv" else args[1] + ".csv"
#         return csv_name


def get_yyyy_mm_dd(csv_name):
    tmp = csv_name[-14:-4].split("-")
    if len(tmp) is not 3:
        print("ERROR: Date in CSV name should be formatted DD-MM-YYYY\nExiting...")
        exit()
    tmp.reverse()
    return "-".join(tmp)


def clean_str(s):
    return s.lower().strip(".").strip()


def get_cities_and_other_data(ordered_dict):
    data = dict(ordered_dict)
    data = dict((clean_str(k), clean_str(v)) for k, v in data.items())
    cities = dict((k, v) for k, v in data.items() if k not in NON_CITY_KEYS and 'unnamed' not in k)
    data = dict((k, v) for k, v in data.items() if k in NON_CITY_KEYS)
    return cities, data


def set_variety(data, curr_variety):
    if 'variety' in data.keys() and data['variety'].strip() is not '':
        curr_variety = data['variety']
    else:
        data['variety'] = curr_variety
    return curr_variety


def make_city_json(result, data, cities, city):
    data["price"] = cities[city]
    data["market"] = city
    result[data['variety'] + "-" + city] = dict((k, v) for k, v in data.items())
    del data["price"]
    del data["market"]


def csv_to_json(csv_name):
    date = get_yyyy_mm_dd(csv_name)
    result = {}
    with open(csv_name, newline='') as csvfile:
        reader = list(csv.DictReader(csvfile, delimiter=","))
        curr_variety = ''
        for ordered_dict in reader:
            cities, data = get_cities_and_other_data(ordered_dict)
            curr_variety = set_variety(data, curr_variety)

            data["code"] = date + "-" + data['commodity']
            data["date"] = date

            for city in cities.keys():
                make_city_json(result, data, cities, city)

        json_name = PATH_TO_JSON_FOLDER / (date + ".json")
        with open(json_name, 'w', newline='') as jsonfile:
            json.dump(result, jsonfile, indent=4, sort_keys=True)
            print("Success. " + str(json_name) + " created.")


# def main():
#     csv_name = parse_args(sys.argv)
#     csv_to_json(csv_name)


