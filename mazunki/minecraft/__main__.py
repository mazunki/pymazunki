#!/usr/bin/env python
# pkg(mazunki)/minecraft/__main__.py
import os

if "PYTHONSTARTUP" in os.environ:
    with open(os.environ["PYTHONSTARTUP"]) as f:
        exec(f.read(), globals())


from . import *
