#!/usr/bin/env python
# pkg(mazunki)/clock/__test__.py

from .chronos import *

t = clock.parse_time("5 days ago")
print(t)

#  vim: set sw=4 ts=4 expandtab
