import os
import configparser
import pkg_resources


def load_config():
    package_conf = pkg_resources.resource_filename(
        pkg_resources.Requirement('pycoins'), 'pycoins.ini'
    )
    homedir_conf = os.path.expanduser('~/.pycoins.ini')
    config_files = [package_conf, homedir_conf]
    config = configparser.RawConfigParser()
    config.read(config_files)
    return config
