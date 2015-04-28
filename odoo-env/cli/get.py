# -*- coding: utf-8 -*-
import argparse
import os
import sys

from openerp.cli import Command
from openerp.modules.module import get_modules

from . import utils


class Get(Command):
    """ Get Odoo modules """

    def get_module(self, module, env_root, exclude=None):
        """ Download and activate module and dependencies """
        # Modules already visited are skipped
        if exclude and module in exclude:
            return True
        exclude = (exclude or ['base']) + [module]
        # Modules already in the path are skipped
        if module in get_modules():
            print('. %s is available from addons path.' % module)
            return True
        # Modules not in the local cache are downloaded
        path = os.path.join(env_root, utils.LOCAL_CACHE)
        module_path = utils.crawl_modules(path).get(module)
        if module_path:
            print('- %s already active (at %s)' % (module, module_path))
        else:
            index = utils.indexed_modules(path)
            if module not in index:
                print('! %s was not found!' % module)
                return False
            utils.download_repo(path, index[module])
            module_path = utils.crawl_modules(path).get(module)
            if not module_path:
                print('! ERROR: %s not found on the repo!' % module)
                return False

        # Symlink module into current environment
        target_path = os.path.join(env_root, module)
        try:
            os.symlink(module_path, target_path)
            print('+ %s activated' % module)
        except OSError:
            print('- %s already exists' % module)

        # Get dependencies
        manifest = utils.load_manifest(module_path)
        depends = manifest['depends']
        for m in depends:
            if not self.get_module(m, env_root, exclude=exclude):
                return False
        return True

    def run(self, cmdargs):
        parser = argparse.ArgumentParser(
            prog="%s get" % os.path.basename(sys.argv[0]),
            description=self.__doc__)
        parser.add_argument(
            'module', help="Name of the module to get")
        #parser.add_argument(
        #    'repo', nargs='?',
        #    help="URL for the source code")

        if not cmdargs:
            sys.exit(parser.print_help())
        args = parser.parse_args(args=cmdargs)

        env_root = os.getcwd()
        self.get_module(args.module, env_root)
        print('Done.')
