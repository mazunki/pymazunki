#!/usr/bin/env python

import itertools

MIN, MAX = 1, 20


@staticmethod
def is_divisible(n: int, by: int) -> bool:
    return n % by == 0


class Mask:
    def __init__(self, conditions):
        self.conditions = conditions

    def __matmul__(self, other):
        return "".join(map(str, itertools.compress(other, self.conditions)))

    def __str__(self):
        return "".join("✅" if bit else "❌" for bit in self.conditions)


class Condition:
    def __init__(self, value: str, by: int):
        self.word = value
        self.function = lambda n: is_divisible(n, by=by)
        self.function.__name__ = f"is_divisible(?, by={by})"

    def __matmul__(self, n):
        return self.function(n)

    def __str__(self):
        return self.word

    def __repr__(self):
        return f"<Condition {self.word}={self.function.__name__} />"


class Fizzer:
    def __init__(self, **cases: int):
        self.cases = [Condition(word, value) for word, value in cases.items()]

    def __rmul__(self, other):
        yield from self.__matmul__(range(1, other + 1))

    def matches(self, n):
        return Mask(condition @ n for condition in self.cases)

    def __matmul__(self, other):
        for n in other:
            yield n, (self.matches(n) @ self.cases or str(n)).title()


for n, word in Fizzer(fizz=3, buzz=5, bazz=7, bizz=11, bim=20) @ range(MIN, MAX + 1):
    print(f"{n:5}: {word}")

#  vim: set sw=4 ts=4 expandtab
