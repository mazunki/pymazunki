#!/usr/bin/env python
# pkg(mazunki)/pythoning/fmt/formatters.py

from typing import Optional, Iterable
import itertools

from ..typed.expressions import Expression, Expressable


class Text:
    def __init__(self, txt):
        self.txt = txt


class LhsRhsExpr(Expression):
    sign: Optional[str] = None

    def __init__(self, lhs: Expressable, rhs: Expressable, sign=None):
        self.lhs = Expression(lhs)
        self.rhs = Expression(rhs)
        if sign:
            self.sign = sign
        elif self.sign is None:
            self.sign = " = "

    def __format__(self, fmt):
        lhsf, _, rhsf = fmt.partition(":")
        lhs = str(self.lhs) if not hasattr(self.lhs, "__format__") else self.lhs
        rhs = str(self.rhs) if not hasattr(self.rhs, "__format__") else self.rhs
        return f"{lhs:{lhsf}}{self.sign}{rhs:{rhsf}}"

    def __str__(self):
        return f"{self.lhs}{self.sign}{self.rhs}"


class EquivalenceExpr(LhsRhsExpr):
    def __init__(self, lhs: Expressable, rhs: Expressable):
        super().__init__(lhs, rhs, " = ")


class DeclarationExpr(LhsRhsExpr):
    def __init__(self, lhs: Expressable, rhs: Expressable):
        super().__init__(lhs, rhs, " := ")


def cell(data, width=None, height=3):
    width = width or len(str(data))
    top = "⎡", " ", "⎤"
    mid = "|", " ", "|"
    bot = "⎣", " ", "⎦"
    if height <= 2:
        return f"{mid[0]}{str(data):^{width}}{mid[1]}"
    else:
        top_line = f"{top[0]}{top[1]:^{width}}{top[2]}"
        data_line = f"{mid[0]}{str(data):^{width}}{mid[2]}"
        pad_line = f"{mid[0]}{mid[1]*width}{mid[2]}"
        bot_line = f"{bot[0]}{bot[1]:^{width}}{bot[2]}"
        padding = (height - 2) // 2

    return (
        top_line,
        *([pad_line] * padding),
        data_line,
        *([pad_line] * padding),
        bot_line,
    )


def cells(datas: Iterable, max=10, *args, **kwargs):
    cells = (cell(data, *args, **kwargs) for data in datas)
    return "\n".join(
        "\n".join([" ".join(line) for line in zip(*itemset)])
        for itemset in itertools.batched(cells, max)
    )


#  vim: set sw=4 ts=4 expandtab
