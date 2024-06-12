#!/usr/bin/env python3.12
# pkg(mazunki)/pythoning/typed/casting.py
import inspect
import functools
from .errors import NoSupportedCasting, NoReturnType

__all__ = ("As", "Cast")


class _Cast:
    def __init__(self):
        self._casts = {}

    def cast(self, func):
        return_type = inspect.signature(func).return_annotation
        if return_type is inspect.Signature.empty:
            raise NoReturnType(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        self._remember(func, return_type)
        return wrapper

    def _remember(self, func, target_type: type):
        self._casts[(func.__qualname__.rsplit(".", 1)[0], target_type)] = func


Cast = _Cast()


def get_caller_generics():
    # this is actually cursed :)
    stack = frame = None
    try:
        stack = inspect.stack()
        frame = stack[2].frame.f_locals
        return frame["self"].__args__

    finally:
        del stack
        del frame


class As[T]:
    def __new__(cls, obj) -> T:
        T = get_caller_generics()[0]
        key = (obj.__class__.__qualname__, T)
        if key in Cast._casts:
            return Cast._casts[key](obj)

        raise NoSupportedCasting(obj, T)


#  vim: set sw=4 ts=4 expandtab
