from typing import Callable
from functools import wraps
from itertools import compress

def cachable(cache_params: list[bool]):
    cache = {}
    def cache_wrapper(fn: Callable):
        @wraps(fn)
        def fn_wrapper(*args):
            key = tuple(compress(args, cache_params))
            if key not in cache:
                cache[key] = fn(*args)
            return cache[key]
        return fn_wrapper
    return cache_wrapper
