import csv
import requests
from urllib import parse
import json

DATA_PATH = 'data/'  # local path
DATA_URL = 'https://19hz.info/'  # online base
DATA_FILES = ['events_BayArea']  # filename
DATA_HEADERS = ["date", "name", "genre", 'location', 'time', 'price',
                'ages', 'promoter', 'url1', 'url2', 'datetime']

def fetch_data():
    for u in DATA_FILES:
        csv_url = parse.urljoin(DATA_URL, u + '.csv')
        csv_local_path = parse.urljoin(DATA_PATH, u + '.csv')
        json_local_path = parse.urljoin(DATA_PATH, u + '.json')

        data = requests.get(csv_url)

        entry_list = list()
        reader = csv.reader(data.text.splitlines())

        for row in reader:
            entry = dict(zip(DATA_HEADERS, row))
            entry_list.append(entry)

        json.dump(entry_list, open(json_local_path, 'w'), indent=4)
        # data = json.load(open(json_local_path))
    return

def update_data():
    for c in DATA_FILES:
        csv_file = parse.urljoin(DATA_PATH, c)

        csvRows = []
        with open(csv_file, "r") as csv_obj:
            reader = csv.reader(csv_obj)
            for row in reader:
                if reader.line_num == 1:
                    continue
                entry = dict(zip(DATA_HEADERS, row))
                csvRows.append(entry)

        for row in csvRows:
            print(row)


if __name__ == '__main__':
    fetch_data()
    # update_data()
