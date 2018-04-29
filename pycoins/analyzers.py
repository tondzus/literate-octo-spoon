import os
import pandas as pd
from pycoins import CONFIG


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
        result.to_csv(output_csv_path, index=False)

    def greatest_relative_closing_span(self):
        data = pd.read_csv(self.csv_path)
        week_data = data.groupby('iso_week')['close']\
            .agg([('min_close', 'min'), ('max_close', 'max')])
        min_close, max_close = week_data['min_close'], week_data['max_close']
        week_data['closing_span'] = (max_close - min_close) / min_close
        return week_data['closing_span'].idxmax()
