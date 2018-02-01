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


if __name__ == '__main__':
    fetch_data()
