import csv
import requests
from urllib import parse
import json

from data import _config as c

def update_data():
    for u in c.DATA_FILES:
        csv_url = parse.urljoin(c.DATA_URL, u + '.csv')
        json_local_path = parse.urljoin(c.DATA_PATH, u[7:] + '.json')

        data = requests.get(csv_url)

        entry_list = list()
        reader = csv.reader(data.text.splitlines())

        for row in reader:
            entry = dict(zip(c.DATA_HEADERS, row))
            entry_list.append(entry)

        json.dump(entry_list, open(json_local_path, 'w'), indent=4)
    return

def fetch_data(location):
    try:
        json_local_path = parse.urljoin(c.DATA_PATH, location + '.json')
        data = json.load(open(json_local_path))
        return data
    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    update_data()
