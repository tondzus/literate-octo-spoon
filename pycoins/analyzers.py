import os
import csv
import pandas as pd
from pycoins import CONFIG, Session
from pycoins.models import MarketEntry
from sqlalchemy import func, desc


class InMemoryAnalyzer:
    def __init__(self):
        self.csv_path = os.path.expanduser(CONFIG.get('data', 'csv_path'))
        if not os.path.isfile(self.csv_path):
            raise ValueError('Data is not available: %s' % self.csv_path)

    def week_close_mean(self, output_csv_path):
        data = pd.read_csv(self.csv_path)
        result = data.groupby('iso_week')['close'].mean()\
            .reset_index().sort_values(by='iso_week')\
            .rename(columns={'close': 'close_mean'})
        result.to_csv(output_csv_path, index=False, line_terminator='\r\n')

    def greatest_relative_closing_span(self):
        data = pd.read_csv(self.csv_path)
        week_data = data.groupby('iso_week')['close']\
            .agg([('min_close', 'min'), ('max_close', 'max')])
        min_close, max_close = week_data['min_close'], week_data['max_close']
        week_data['closing_span'] = (max_close - min_close) / min_close
        return week_data['closing_span'].idxmax()


class SQLiteAnalyzer:
    def week_close_mean(self, output_csv_path):
        session = Session()
        query = session.query(
            MarketEntry.iso_week, func.avg(MarketEntry.close)
        ).group_by(MarketEntry.iso_week).order_by('iso_week')

        with open(output_csv_path, 'w', newline='') as fp:
            csv_writer = csv.writer(fp)
            csv_writer.writerow(['iso_week', 'close_mean'])
            for row in query:
                csv_writer.writerow(row)

    def greatest_relative_closing_span(self):
        session = Session()
        min_close = func.min(MarketEntry.close)
        max_close = func.max(MarketEntry.close)

        formula = (max_close - min_close) / min_close
        query = session.query(
            MarketEntry.iso_week, formula.label('relativespan')
        ).group_by(
            MarketEntry.iso_week
        ).order_by(
            desc('relativespan')
        ).limit(1)
        return query.first()[0]
