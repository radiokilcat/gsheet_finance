import csv
from datetime import datetime
import pandas as pd


def get_expenses_from_csv(file_obj):
    reader = csv.reader(file_obj, delimiter=";")
    header = next(reader)
    result = {}

    for row in reversed(list(reader)):
        dt = datetime.date(datetime.strptime(row[0], '%d.%m.%Y %H:%M:%S'))
        value = float(row[6].replace(',', '.'))
        if value <= 0:
            if result.get(dt) is None:
                result[dt] = value
            else:
                result[dt] += value

    return result

