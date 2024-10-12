#!/usr/bin/env python

import pathlib
import platform
import readline  # ignore: reportUnusedImport
import rlcompleter

from mazunki import xdg


def interactive_hook():
    readline_doc = getattr(readline, "__doc__", "")
    if readline_doc is not None and "libedit" in readline_doc:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")


def get_python_info(version=False) -> str:
    if version:
        return f"python v{platform.python_version()} [{platform.python_compiler().strip()}]"
    else:
        return f" python interpreter v{platform.python_version()}"


def ready_history_file(_history, _python_rtp):
    try:
        readline.read_history_file(_history)
    except FileNotFoundError:
        print("couldn't read history!", _history)
        pathlib.Path(_python_rtp).mkdir(parents=True, exist_ok=True)


def ready_startup(_python_rtp):
    _history = pathlib.Path(_python_rtp).joinpath("history")
    ready_history_file(_history, _python_rtp)
    return {"rtp": _python_rtp, "history": _history}


def cleanup(_state):
    print("byeeee 😿")
    readline.write_history_file(_state["history"])


#  vim: set sw=4 ts=4 expandtab
