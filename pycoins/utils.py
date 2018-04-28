import os
import configparser
import pkg_resources
from sqlalchemy import create_engine


def load_config():
    package_conf = pkg_resources.resource_filename(
        pkg_resources.Requirement('pycoins'), 'pycoins.ini'
    )
    homedir_conf = os.path.expanduser('~/.pycoins.ini')
    config_files = [package_conf, homedir_conf]
    config = configparser.RawConfigParser()
    config.read(config_files)
    return config


def init_db_engine(config):
    sqlite_path = os.path.expanduser(config.get('data', 'sqlite_path'))
    os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
    sqlalchemy_engine = 'sqlite:///%s' % sqlite_path
    return create_engine(sqlalchemy_engine)
