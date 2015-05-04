# -*- coding: utf-8 -*-
from __future__ import print_function

import ast
import os
import yaml
from openerp.modules.module import MANIFEST


LOCAL_CACHE = '.ooenv-local'


def crawl_modules(path):
    """ Crawls inside a path to return a map of modules to paths """

    def path_is_module(path):
        files = os.listdir(path)
        return MANIFEST in files and '__init__.py' in files

    # Avoid empty basename when path ends with slash
    if not os.path.basename(path):
        path = os.path.dirname(path)

    res = {}
    if os.path.isdir(path) and not os.path.basename(path)[0] == '.git':
        for x in os.listdir(path):
            pathx = os.path.join(path, x)
            if not os.path.isdir(pathx):
                continue
            if path_is_module(pathx):
                # not checking if module is installable; should we?
                res[x] = pathx
            else:
                res.update(crawl_modules(pathx))
    return res


def indexed_modules(path):
    index = {}
    for x in os.listdir(path):
        x_path = os.path.join(path, x)
        if os.path.isdir(x_path):
            index.update(
                indexed_modules(x_path))
        else:
            if x.endswith('.index'):
                x_index = yaml.load(open(x_path))
                index.update(x_index)
    return index


def load_manifest(module_path):
    path = os.path.join(module_path, MANIFEST)
    return ast.literal_eval(
        open(path).read())
