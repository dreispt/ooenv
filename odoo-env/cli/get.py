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
        exclude = exclude if exclude is not None else ['base']
        exclude.append(module)
        # Modules already in the path are skipped
        if module in get_modules():
            print('. %s is available from addons path.' % module)
            return True
        if module in os.listdir(env_root):
            # Modules in the env root are already active
            module_path = os.path.join(env_root, module)
            print('. %s already active (at %s)' % (module, module_path))

        else:
            # Modules in the local cache are available to activate
            path = os.path.join(env_root, utils.LOCAL_CACHE)
            module_path = utils.crawl_modules(path).get(module)
            if not module_path:
                # Modules not in the local cache are downloaded
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
        if module not in os.listdir(env_root):
            target_path = os.path.join(env_root, module)
            os.symlink(module_path, target_path)
            print('+ %s activated (from %s)' % (module, module_path))

        # Get dependencies
        try:
            manifest = utils.load_manifest(module_path)
        except IOError:
            manifest = {}
        depends = manifest.get('depends')
        for m in depends:
            if not self.get_module(m, env_root, exclude=exclude):
                return False
        return True

    def get_modules(self, modules, env_root, exclude=None):
        exclude = exclude or ['base']
        for m in modules:
            self.get_module(m, env_root, exclude)
        return True

    def run(self, cmdargs):
        parser = argparse.ArgumentParser(
            prog="%s get" % os.path.basename(sys.argv[0]),
            description=self.__doc__)
        parser.add_argument(
            'modules', nargs='+', help="Modules to get")
        parser.add_argument('-q', '--quiet', dest='quiet',
                            help='Suppress information messages')
        parser.add_argument('-v', '--verbose', dest='verbose',
                            help='Verbose messages')

        if not cmdargs:
            sys.exit(parser.print_help())
        args = parser.parse_args(args=cmdargs)

        env_root = os.getcwd()
        self.get_modules(args.modules, env_root)
        print('Done.')
