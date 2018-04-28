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


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

download_parser = subparsers.add_parser('download')
download_parser.add_argument('--api-key',
                             help='Used for REST api authentication')
download_parser.set_defaults(command=download_command)

args = parser.parse_args()
args.command(args)
