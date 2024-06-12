#!/usr/bin/env python

from typing import Iterable, Iterator
from ..typed.errors import UnexpectedData

type OneOrMany[T] = T | Iterable[T]


def flatten[T](type_: type[T], *objs: OneOrMany[T]) -> Iterator[T]:
    for obj in objs:
        if isinstance(obj, type_):
            yield obj
        elif isinstance(obj, Iterable):
            yield from flatten(type_, *obj)
        else:
            UnexpectedData("{obj} is not of expected type")


#  vim: set sw=4 ts=4 expandtab
