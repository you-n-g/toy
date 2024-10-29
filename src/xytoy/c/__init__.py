"""Tools to control the workflow of Python program"""

import time


def wait_retry(retry_n=3, sleep_time=1):
    """Decorator to wait and retry the function for retry_n times

    Example:
    >>> import time
    >>> @wait_retry(retry_n=2, sleep_time=1)
    ... def test_func():
    ...     global counter
    ...     counter += 1
    ...     if counter < 3:
    ...         raise ValueError("Counter is less than 3")
    ...     return counter
    >>> counter = 0
    >>> try:
    ...     test_func()
    ... except ValueError as e:
    ...     print(f"Caught an exception: {e}")
    Error: Counter is less than 3
    Error: Counter is less than 3
    Caught an exception: Counter is less than 3
    >>> counter
    2
    """

    def decorator(f):
        def wrapper(*args, **kwargs):
            for i in range(retry_n):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(sleep_time)
                    if i == retry_n - 1:
                        raise e

        return wrapper

    return decorator
