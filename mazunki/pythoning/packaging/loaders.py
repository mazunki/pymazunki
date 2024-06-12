#!/usr/bin/env python

from typing import Optional
from types import ModuleType
from importlib import import_module
import sys


def loadmod(package: str, *modules: str) -> Optional[ModuleType | list[ModuleType]]:
    try:
        if len(modules) == 1:
            return getattr(import_module(package), modules[0])
        elif len(modules) >= 2:
            return [getattr(import_module(package), mod) for mod in modules]
        return import_module(package)
    except ModuleNotFoundError as err:
        print(f"no findy {err.name} 😭", file=sys.stderr)


#  vim: set sw=4 ts=4 expandtab
