#!/usr/bin/env sh
rm -rf ./test-env
../odoo/odoo.py env test-env
./test-env/odoo.sh get --verbose document_page mgmtsystem
ls -l ./testenv

./test-env/odoo.sh start --stop-after-init
