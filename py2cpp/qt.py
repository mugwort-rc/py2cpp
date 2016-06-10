# -*- coding: utf-8 -*-

from PyQt4 import Qt

from . import cpp


for name in dir(Qt):
    if not name.startswith("Q"):
        continue
    cpp.type_registry.register(name, "{} *".format(name))
