#!/usr/bin/env python
from itertools import batched


def nib(num: int):
    return " ".join(
        ''.join(nib) for nib in batched(reversed(format(num, "b")), 4)
    )[::-1]

