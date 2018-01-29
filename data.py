import csv
from urllib import parse

DATA_PATH = 'data/'
DATA_CSV = ['events_BayArea.csv']

file = open(parse.urljoin(DATA_PATH, DATA_CSV[0]))
reader = csv.reader(file)
data = list(reader)
print(data)
