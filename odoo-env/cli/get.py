# -*- coding: utf-8 -*-
import argparse
import os
import sys

from openerp.cli import Command
# from openerp.modules.module import (get_module_root, MANIFEST, load_information_from_description_file as load_manifest)


class Get(Command):
    """ Get Odoo modules """

    def get_module(self, module, repo=None):
        return

    def run(self, cmdargs):
        parser = argparse.ArgumentParser(
            prog="%s get" % sys.argv[0].split(os.path.sep)[-1],
            description=self.__doc__,
        )
        parser.add_argument('module', help="Name of the module to get")
        parser.add_argument(
            'repo', nargs='?',
            help="URL for the source code")

        if not cmdargs:
            sys.exit(parser.print_help())
        args = parser.parse_args(args=cmdargs)

        return self.get_module(args.module, args.repo)
