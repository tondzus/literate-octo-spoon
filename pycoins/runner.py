from pycoins import datasources, analyzers


def get_analyzer(engine):
    return {
        'memory': analyzers.InMemoryAnalyzer,
    }[engine]


def download_data(api_key):
    downloader = datasources.Alphavantage(api_key)
    downloader.store_data()


def mean_week_closing_price(engine, output_csv_path):
    analyzer_cls = get_analyzer(engine)
    analyzer = analyzer_cls()
    analyzer.week_close_mean(output_csv_path)


def greatest_relative_price(engine):
    analyzer_cls = get_analyzer(engine)
    analyzer = analyzer_cls()
    return analyzer.greatest_relative_closing_span()
