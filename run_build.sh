#!/usr/bin/env sh
~/odoo-8.0/odoo.py env testenv
./testenv/odoo.sh get mgmtsystem
ls -l ./testenv

./testenv/odoosh start --stop-after-init
