#!/usr/bin/env python
# pkg(mazunki)/pythoning/packaging/library.py

import os
import pkgutil
from typing import Self, Iterable

import abc

# from ..typed.errors import
from ..typed.collections import OneOrMany, flatten


class Module:
    def __init__(self, mod: pkgutil.ModuleInfo):
        self.mod = mod

    def __format__(self, fmt) -> str:
        if fmt == "%p":
            return str(self.mod.module_finder)
        elif fmt == "%n":
            return str(self.mod.name)

        return f"{self:%n}"

    def __str__(self):
        return f"{self}"

    def _eq__(self, other: Self | str):
        if isinstance(other, str):
            return self.mod.name == other
        elif isinstance(other, Self):
            return self.mod == other.mod
        return False

    def __hash__(self) -> int:
        return hash(self.mod)

    @property
    def name(self):
        return self.mod.name

    @property
    def paths(self):
        return self.mod.module_finder

    @property
    def is_builtin(self):
        path = self.mod.module_finder.path
        return path == os.path.dirname(os.__file__)

    @property
    def is_special(self):
        return self.mod.name.startswith("_")


class LibrarySet(abc.ABC):
    libs: set[Module]

    def __init__(self, *modules: OneOrMany[Module]):
        self.libs = set(flatten(Module, *modules))

    def __iter__(self) -> Iterable[Module]:
        yield from self.libs

    def __neg__(self, other: Self):
        return self.__class__(set(mod for mod in self.libs - other.libs))

    def __str__(self):
        return f"({", ".join(map(str, self.libs))})"


class AllModules(LibrarySet):
    def __init__(self):
        super().__init__(*(Module(mod) for mod in pkgutil.iter_modules()))


class Builtins(LibrarySet):
    def __init__(self):
        libs = (Module(lib) for lib in pkgutil.iter_modules())
        libs = (lib for lib in libs if lib.is_builtin)
        super().__init__(set(libs))


class Installed(LibrarySet):
    def __init__(self):
        libs = (Module(lib) for lib in pkgutil.iter_modules())
        libs = (lib for lib in libs if not lib.is_builtin)
        super().__init__(set(libs))


all_libs = AllModules()
# print(all_libs)

builtins = Builtins()
print("Built-in packages:", builtins)

installed = Installed()
print("Installed-packages:", installed)


#  vim: set sts=4 sw=4 ts=4 expandtab
