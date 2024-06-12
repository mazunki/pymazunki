#!/usr/bin/env python

import datetime
from ..calculate import Time


def how_long(goal, rate, start=0):
    total_seconds = (goal - start) / rate
    return Time(seconds=total_seconds)


#  vim: set sw=4 ts=4 expandtab
