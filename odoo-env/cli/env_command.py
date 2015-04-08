# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from __future__ import print_function
import argparse
import os
import sys
import openerp


class Env(openerp.cli.Command):
    """Create a new Odoo addons environment"""

    def run(self, cmdargs):
        parser = argparse.ArgumentParser(
            prog="%s env" % sys.argv[0].split(os.path.sep)[-1],
            description=self.__doc__,
        )
        parser.add_argument(
            'path', nargs='?',
            help="Path of the addons directory to create")

        if not cmdargs:
            sys.exit(parser.print_help())
        args = parser.parse_args(args=cmdargs)
        odoo_path = os.path.realpath(sys.argv[0])
        env_path = os.path.realpath(args.path)
        env_fname = os.path.join(env_path, 'odoo')
        env_db = env_path.split(os.path.sep)[-1]
        env_script = '\n'.join([
            "#!/usr/bin/env bash",
            "python %s start --path=%s -d %s $*" %
            (odoo_path, env_path, env_db)
        ])
        os.mkdir(args.path)
        open(env_fname, 'w').write(env_script)

        print(sys.argv)
        print('Created environment %s using Odoo at %s' %
              (args.path, odoo_path))
