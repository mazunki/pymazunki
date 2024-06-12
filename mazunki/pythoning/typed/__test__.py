#!/usr/bin/env python
# pkg(mazunki)/pythoning/typed/__test__.py

from .casting import As, Cast
from .static import typechecked, constrained
from typing import Any


class SomeClass:
    def __init__(self, val: Any):
        self.value = val

    @Cast.cast
    def lol_lmao(self) -> int:
        return int(self.value)


obj = SomeClass("5")

ret = As[int](obj)
print(repr(ret))


@typechecked
def is_even(number: int):
    return number % 2 == 0


@typechecked
@constrained("a", is_even)
@constrained("b", is_even)
def add_even_numbers(a: int, b: int):
    print(f"Adding {a} + {b} of types {type(a)} + {type(b)}")
    print(a + b)


add_even_numbers(1, 2)

#  vim: set sw=4 ts=4 expandtag
