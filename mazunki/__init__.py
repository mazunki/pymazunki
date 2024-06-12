#!/usr/bin/env python
# pkg(mazunki)/__init__.py

from .pythoning.fmt.clear import clear
from .pythoning.fmt.printing import print as pprint
from .pythoning.typed import errors, collections, casting, static
from .pythoning import xdg

__all__ = ("clear", "pprint", "errors", "collections", "casting", "static", "xdg")

#  vim: set sw=4 ts=4 expandtab
