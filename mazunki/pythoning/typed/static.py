#!/usr/bin/env python
# pkg(mazunki)/typed/static.py

from typing import Callable, Any
import functools


class StaticTypeError(Exception):
    def __init__(self, invalid_value, annotation):
        self.parameter, self.expected_type = annotation
        message = f"{self.parameter}={repr(invalid_value)} is not of expected type {self.expected_type}"
        super().__init__(message)


class TypeConstraintError(Exception):
    def __init__(self, invalid_value, callback: Callable, name):
        message = f"{name}={repr(invalid_value)} failed {callback.__name__}"
        super().__init__(message)


def assert_type(value: Any, annotation: tuple[str, type]):
    _, expected_type = annotation
    if expected_type is None:
        return
    if not isinstance(value, expected_type):
        raise StaticTypeError(value, annotation)


def check_arguments(func: Callable, *args):
    for pos, arg in enumerate(args):
        param_name = list(func.__annotations__)[pos]
        annotation = param_name, func.__annotations__[param_name]

        assert_type(arg, annotation)


def check_keyword_arguments(func: Callable, **kwargs):
    for name, kwarg in kwargs.items():
        annotation = name, func.__annotations__[name]
        assert_type(kwarg, annotation)


def check_return(func: Callable, value: type):
    var_type = func.__annotations__.get("return", None)
    assert_type(value, ("return", var_type))


def typechecked(func):
    def _typechecker(*args, **kwargs):
        check_arguments(func, *args)
        check_keyword_arguments(func, **kwargs)

        result = func(*args, **kwargs)
        check_return(func, type(result))
        return result

    return _typechecker


def check_constraint(value, callback, name, *args, **kwargs):
    if not callback(value, *args, **kwargs):
        raise TypeConstraintError(value, callback, name)


@typechecked
def constrained(param_name: str, callback: Callable, *cb_args, **cb_kwargs):
    def _wrapper(func: Callable):
        @functools.wraps(func)
        def _constrainer(*args, **kwargs):
            if param_name in kwargs:
                check_constraint(
                    kwargs[param_name], callback, param_name, *cb_args, **cb_kwargs
                )
            else:
                for pos, arg in enumerate(args):
                    if param_name == list(func.__annotations__)[pos]:
                        check_constraint(
                            arg, callback, param_name, *cb_args, **cb_kwargs
                        )
                        break
            return func(*args, **kwargs)

        return _constrainer

    return _wrapper


#  vim: set sw=4 ts=4 expandtab
