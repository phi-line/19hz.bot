DATA_PATH = 'data/'  # local path
DATA_URL = 'https://19hz.info/'  # online base
DATA_FILES = ['events_BayArea', 'events_LosAngeles', 'events_Atlanta',
              'events_Texas', 'events_Miami', 'events_Massachusetts']
DATA_SHORT = ['BayArea', 'LosAngeles', 'Atlanta', 'Texas', 'Miami', 'Massachusetts']
DATA_HEADERS = ["date", "name", "genre", 'location', 'time', 'price',
                'ages', 'promoter', 'url1', 'url2', 'datetime']

ICON_URL = "https://raw.githubusercontent.com/phi-line/19hz.bot/master/logo.png"

DATA_ALIAS = {'BayArea':['bay', 'area', 'ba', 'b', 'sanfrancisco', 'sanfran',
                         'san', 'francisco' 'sf', 'oakland', 'oak', 'san jose', 'sj'],
              'LosAngeles':['la', 'los', 'angeles', 'hell'],
              'Atlanta':['bacon', 'georgia'],
              'Texas':['houston', 'austin'],
              'Miami':['florida'],
              'Massachusetts':['boston']}