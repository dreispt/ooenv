[![Build Status](https://travis-ci.org/dreispt/ooenv.svg)](https://travis-ci.org/dreispt/ooenv)

Odoo Environment and Package Manager
====================================

Add a feature similar to Pyhton’s virtualenv + pip.

The `env` command creates a new Odoo environment: a directory for Odoo addons 
to be the home for a database. It contains an `odoo.sh` to be used to work
with this environment.

The `get` command discovers modules and makes them available in an Odoo
environment addons. For this it uses an index of known modules, downloads
the source code from the web, and makes the available in the environment
through a symlink.

The default index used is: https://github.com/dreispt/ooenv-index
For the moment only OCA modules are indexed.

To run an Odoo server for that environment, and maybe perform some actions on it
such as modules installation or upgrade, use the `./odoo.sh` with the
`start` CLI command:

    $ ./odoo.sh start

This automatically appends the environment directory to the addons path and uses
the directory name for the database name.


Installation
------------
To install just put the `odoo-env` module somewhere in your
addons path. The module provides additional Odoo CLI commands and
no actual installation is needed.

To confirm the commands are available try:

    $ ./path-to-odoo/odoo.py env -h

There are some known issues with CLI commands on Odoo 8.0.
You may need to add this fix to you Odoo server: https://github.com/odoo/odoo/pull/6335


Quickstart
----------

To better understand how to get started, here is an example session.

First we create a new Odoo environment. 
The new Odoo environment will be tied to a particular Odoo server.
The one used to run the `env` command will be used as the reference server:

    $ ./path-to-odoo/odoo.py env my-name

A `my-name` subdirectory will be created with an `odoo.sh` executable
file. Further actions for that environment should be ran using that script.

Now we will install the `mgmtsystem` OCA module with all it’s dependencies.

    $ my-name/odoo.sh get mgmtsystem

You will notice that the OCA/management-system and OCA/knowlege repositories
will be automatically cloned into a local cache to provide the needed modules.

If you now list the contents of the `my-name/` directory, you will see the two
modules needed.

To start the server for this environment and install `mgmtsystem`:

    $ my-name/odoo.sh start -i mgmtsystem
