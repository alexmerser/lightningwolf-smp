#!/usr/bin/env python
# coding=utf8
"""Lightningwolf Server Management Panel

Usage:
  smp.py [--config=<config>] start
  smp.py init:config
  smp.py [--config=<config>] init:db
  smp.py [--config=<config>] (user:create | user:password | user:delete) <username>
  smp.py (-h | --help)
  smp.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --credential=C  The C credential [default: admin] (admin|user)

"""
import os
from docopt import docopt
from lightningwolf_smp import version


def main():
    arguments = docopt(__doc__, version=version)
    if arguments['--config'] is not None:
        os.environ["LIGHTNINGWOLF_SETTINGS"] = arguments['--config']

    if arguments['start']:
        from lightningwolf_smp.run import main
        main()
    else:
        from lightningwolf_smp.utils.console import parse_arguments
        parse_arguments(arguments)

if __name__ == '__main__':
    main()
