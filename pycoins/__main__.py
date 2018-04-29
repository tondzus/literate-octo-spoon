import os
import logging
import argparse
from pycoins import runner, CONFIG


def init_logging():
    logpath = os.path.expanduser(CONFIG.get('logging', 'path'))
    loglevel = CONFIG.get('logging', 'level').upper()
    logformat = CONFIG.get('logging', 'format')
    os.makedirs(os.path.dirname(logpath), exist_ok=True)
    logging.basicConfig(filename=logpath, level=getattr(logging, loglevel),
                        format=logformat)


def download_command(args):
    init_logging()
    runner.download_data(args.api_key)


def analyze_command(args):
    init_logging()
    if args.analysis == 'week-means':
        if not args.output_csv:
            print('--output-csv has to be set for week-means. Exiting.')
            exit(1)
        runner.mean_week_closing_price(args.engine, args.output_csv)
    if args.analysis == 'greatest-span':
        print(runner.greatest_relative_price(args.engine))


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

download_parser = subparsers.add_parser('download')
download_parser.add_argument('--api-key',
                             help='Used for REST api authentication')
download_parser.set_defaults(command=download_command)

analyze_parser = subparsers.add_parser('analyze')
analyze_parser.add_argument('engine', choices=['memory'])
analyze_parser.add_argument('analysis', choices=['week-means', 'greatest-span'])
analyze_parser.add_argument('--output-csv', default=None,
                            help='Week mean prices will be stored here')
analyze_parser.set_defaults(command=analyze_command)


args = parser.parse_args()
args.command(args)
