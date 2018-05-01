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


def challenge_command(args):
    init_logging()
    print('Downloading data')
    runner.download_data(args.api_key)

    grp_memory = runner.greatest_relative_price('memory')
    grp_sqlite = runner.greatest_relative_price('sqlite')
    print('Greatest relative price week (memory):', grp_memory)
    print('Greatest relative price week (sqlite):', grp_sqlite)

    os.makedirs(os.path.abspath(args.output_folder), exist_ok=True)
    memory_csv = os.path.join(
        args.output_folder, 'mean_week_price_memory.csv'
    )
    sqlite_csv = os.path.join(
        args.output_folder, 'mean_week_price_sqlite.csv'
    )
    runner.mean_week_closing_price('memory', memory_csv)
    print('Wrote memory computed mean week prices to', memory_csv)
    runner.mean_week_closing_price('sqlite', sqlite_csv)
    print('Wrote sqlite computed mean week prices to', sqlite_csv)

    print('Challenge done!')


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

download_parser = subparsers.add_parser('download')
download_parser.add_argument('--api-key',
                             help='Used for REST api authentication')
download_parser.set_defaults(command=download_command)

analyze_parser = subparsers.add_parser('analyze')
analyze_parser.add_argument('engine', choices=['memory', 'sqlite'])
analyze_parser.add_argument('analysis', choices=['week-means', 'greatest-span'])
analyze_parser.add_argument('--output-csv', default=None,
                            help='Week mean prices will be stored here')
analyze_parser.set_defaults(command=analyze_command)

complete_parser = subparsers.add_parser('challenge')
complete_parser.add_argument('--api-key',
                             help='Used for REST api authentication')
complete_parser.add_argument('--output-folder', default='.',
                             help='Mean week prices will be stored here.')
complete_parser.set_defaults(command=challenge_command)


args = parser.parse_args()
args.command(args)
