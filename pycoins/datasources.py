import os
import logging
import requests
from pycoins import config


class Alphavantage:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = config.get('alphavantage', 'url').format(api_key=api_key)
        self.csv_path = os.path.expanduser(config.get('data', 'csv_path'))

    def store_data(self):
        log = logging.getLogger(__name__)
        log.info('Going to store data from %s to %s',
                 self.url.replace(self.api_key, 'TOKEN'), self.csv_path)
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        res = requests.get(self.url, stream=True)
        with open(self.csv_path, 'wb') as fp:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    fp.write(chunk)
