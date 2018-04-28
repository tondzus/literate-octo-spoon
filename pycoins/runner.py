from pycoins import datasources


def download_data(api_key):
    downloader = datasources.Alphavantage(api_key)
    downloader.store_data()
