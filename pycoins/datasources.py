import os
import csv
import logging
import requests
import datetime
from pycoins import CONFIG, models, Session


class Alphavantage:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = CONFIG.get('alphavantage', 'url').format(api_key=api_key)
        self.csv_path = os.path.abspath(
            os.path.expanduser(CONFIG.get('data', 'csv_path'))
        )

    def _extract_from_date_dict(self, original_date_dict):
        return {
            'open': original_date_dict['1a. open (USD)'],
            'close': original_date_dict['4a. close (USD)'],
            'low': original_date_dict['3a. low (USD)'],
            'high': original_date_dict['2a. high (USD)'],
            'volume': original_date_dict['5. volume'],
            'market_cap': original_date_dict['6. market cap (USD)'],
            'symbol': 'BTC', 'market': 'USD',
        }

    def _write_csv(self, date_map):
        log = logging.getLogger(__name__)
        log.debug('Writing data to %s', self.csv_path)
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        strptime = datetime.datetime.strptime
        with open(self.csv_path, 'w', newline='') as fp:
            csv_writer = csv.writer(fp)
            header = [
                'date', 'iso_week', 'symbol', 'market', 'open', 'close',
                'high', 'low', 'volume', 'market_cap'
            ]
            csv_writer.writerow(header)
            for date, date_dict in date_map.items():
                csv_row = self._extract_from_date_dict(date_dict)
                csv_row['date'] = date
                date_obj = strptime(date, '%Y-%m-%d').date()
                csv_row['iso_week'] = '%d-W%02d' % date_obj.isocalendar()[:2]
                csv_writer.writerow([csv_row[h] for h in header])

    def _write_sqlite(self, date_map):
        session = Session()
        objects = []
        log = logging.getLogger(__name__)
        log.debug('Writing data to %s', session.bind.url)

        strptime = datetime.datetime.strptime
        for date, date_dict in date_map.items():
            csv_row = self._extract_from_date_dict(date_dict)
            csv_row['date'] = strptime(date, '%Y-%m-%d').date()
            csv_row['iso_week'] = '%d-W%02d' % csv_row['date'].isocalendar()[:2]
            rec = models.MarketEntry(**csv_row)
            objects.append(rec)

            if len(objects) > 1000:
                session.bulk_save_objects(objects)
                session.commit()
                objects = []

        if objects:
            session.bulk_save_objects(objects)
            session.commit()

    def store_data(self):
        log = logging.getLogger(__name__)
        log.info('Going to query data from %s',
                 self.url.replace(self.api_key, 'TOKEN'))

        res = requests.get(self.url)
        date_map = res.json()['Time Series (Digital Currency Daily)']

        self._write_csv(date_map)
        self._write_sqlite(date_map)
