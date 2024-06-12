#!/usr/bin/env python
from .clock import *

import sys

_, *args = sys.argv


def time_from(times, arg):
    if arg.startswith("%"):
        tname = arg[1:]
        return times, tname

    anonymous_keys = [
        tname.partition("t")[2] for tname in times.keys() if tname.startswith("__")
    ]
    __last_anon = max(anonymous_keys) if anonymous_keys else 0
    if arg.startswith("--") and "=" in arg:
        tname, _, tfmt = arg[2:].partition("=")
    else:
        tname, tfmt = f"__t{int(__last_anon)+1}", arg

    t = Time.parse(tfmt)
    times[tname] = t
    return times, tname


def parse_args(args):
    mode = "print"
    times = {}
    units = []
    recognized_modes = {"add", "subtract"}
    mode = None

    u = []
    for arg in args:
        if arg in recognized_modes:
            if u:
                units.append((mode if mode else arg, u))
            u = []
            mode = arg
        else:
            times, time = time_from(times, arg)
            if mode:
                u.append(time)

    if u:
        units.append((mode, u))
    return times, units


times, tasks = parse_args(args)
print(times, tasks, sep="\n")

results = []
for mode, batch in tasks:
    car, cdr = batch[0], batch[1:]

    b = [times[car]]
    for name in cdr:
        time = times[name]
        if mode == "add":
            b.append(b[-1] + time)
        elif mode == "subtract":
            b.append(b[-1] - time)

    results.append((mode, b))


for action, times in results:
    print(action)
    for time in times:
        print("\t", time)

#  vim: set sw=4 ts=4 expandtab
