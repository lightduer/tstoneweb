# -*- coding: utf-8 -*-
import functools


def blueprint_usage(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        pass
        return func(*args, **kwargs)
    return _wrapper
