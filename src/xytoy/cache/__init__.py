"""Cache module for xytoy package."""

import hashlib
import inspect
import os
import pickle
from typing import Any, Callable, Optional


def calculate_cache_key(func: Callable[..., Any], args: Any, kwargs: Any) -> str:
    """Calculate a unique hash key for the function URI and arguments.

    Args:
        func (Callable[..., Any]): The function for which the cache key is being calculated.
        args (Any): Positional arguments for the function.
        kwargs (Any): Keyword arguments for the function.

    Returns:
        str: A unique hash string representing the function arguments.
    """
    func_uri = f"{func.__module__}.{func.__qualname__}"
    func_code = inspect.getsource(func)
    hash_input = func_uri + func_code + str(args) + str(kwargs)
    return hashlib.sha256(hash_input.encode()).hexdigest()


def cache(func: Optional[Callable[..., Any]] = None, cache_folder: Optional[str] = None) -> Callable[..., Any]:
    """Decorator to cache the result of a function call.

    This uses a hash of the function arguments to create a unique filename and store
    the return value in a cache file.

    .. code-block:: python

        cache(f)(aa, bb)

        @cache(cache_folder=cc)
        def f(...):
            ...

    Args:
        func (Callable[..., Any]): The function to be decorated.
        cache_folder (Optional[str]): The folder where cache files will be stored.
                                      If None, the folder of the calling script is used.

    Returns:
        Callable[..., Any]: The wrapped function with caching capability.
    """
    if callable(func):

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper function to handle caching logic.

            Args:
                *args (Any): Positional arguments for the function.
                **kwargs (Any): Keyword arguments for the function.

            Returns:
                Any: The result of the function call, either from cache or freshly computed.
            """
            # Create a unique hash for the function URI and arguments
            hash_value = calculate_cache_key(func, args, kwargs)

            # Determine the cache file path
            _cache_folder = cache_folder if cache_folder is not None else os.path.dirname(inspect.stack()[1].filename)
            cache_file = os.path.join(_cache_folder, f"{hash_value}.pkl")

            if os.path.exists(cache_file):
                # Warning: Using pickle can be unsafe with untrusted data.
                with open(cache_file, "rb") as f:
                    return pickle.load(f)  # Warning: Using pickle can be unsafe with untrusted data. noqa: S301

            result = func(*args, **kwargs)
            with open(cache_file, "wb") as f:
                pickle.dump(result, f)
            return result

        return wrapper
    else:
        return lambda f: cache(f, cache_folder)
