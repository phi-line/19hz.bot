import csv
import requests
from urllib import parse

DATA_PATH = 'data/'  # local path
DATA_URL = ''
DATA_CSV = ['events_BayArea.csv']  # filename
DATA_HEADERS = ["date", "name", "genre", 'location', 'time', 'price',
                'ages', 'promoter', 'url1', 'url2', 'datetime']

def fetch_data():
    CSV_URL = 'http://samplecsvs.s3.amazonaws.com/Sacramentorealestatetransactions.csv'

    with requests.Session() as s:
        download = s.get(CSV_URL)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list
    return

def update_data():
    for c in DATA_CSV:
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
    update_data()
