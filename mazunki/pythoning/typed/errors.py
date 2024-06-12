#!/usr/bin/env python
# pkg(mazunki)/pythoning/typed/errors.py


class NoReturnType(ValueError):
    def __init__(self, func):
        super().__init__(f"No return type given for {func.__name__}")


class NoSupportedCasting(TypeError):
    def __init__(self, obj, target):
        super().__init__(
            f"No conversion found for {type(obj).__name__} to {target.__name__}"
        )


class UnexpectedData(TypeError):
    def __init__(self, data):
        super().__init__(f"wasn't expecting {type(data)}")


#  vim: set sw=4 ts=4 expandtab
