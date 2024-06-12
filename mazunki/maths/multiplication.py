#!/usr/bin/env python

from ..pythoning.fmt.formatters import cells


def times_table(a: int, max: int = 10) -> None:
    len_rhs = len(str(a * max))
    len_b = len(str(max))
    for b in range(max + 1):
        result = a * b
        lhs = f" {a} × {b:>{len_b}}"
        rhs = f"{result}"
        print(f"{lhs:<4} = {rhs:>{len_rhs}}")


def multiply_to(n: int, using: int):
    print(cells(range(1, n + 1), max=using, width=5))


#  vim: set sw=4 ts=4 expandtab
