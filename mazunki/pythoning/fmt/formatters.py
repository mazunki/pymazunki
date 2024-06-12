#!/usr/bin/env python

import warnings


class MalformedString(Warning): ...


class Formatter:
    def __init__(self, specifiers):
        self.specifiers = specifiers

    def format(self, string: str):
        it = enumerate(string)
        stringbuilder = []

        for i, character in it:
            if character == "%":
                if i + 1 >= len(string):
                    warnings.warn(
                        f"{repr(string)} ends with an unfinished format specifier",
                        MalformedString,
                    )
                    continue
                if string[i + 1] in self.specifiers:
                    stringbuilder.append(self.specifiers[string[i + 1]])
                    next(it)
            elif character == "{":
                if string[i + 1] in self.specifiers:
                    stringbuilder.append(self.specifiers[string[i + 1]])
                    next(it)
            else:
                stringbuilder.append(character)

        return "".join(map(str, stringbuilder))


def test():
    specifiers = {
        "h": "hey",
        "x": "world",
        "v": "awesome",
        "f": 69,
    }
    text = "Hey! '%h' is a very '%x'. %f%"
    f = Formatter(specifiers).format(text)
    print(f)


#  vim: set sw=4 ts=4 expandtab
