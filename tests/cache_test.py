"""Tests for the cache module."""

import os
import pickle
import tempfile

from xytoy.cache import cache, calculate_cache_key


def test_cache_decorator() -> None:
    """Test the cache decorator."""
    # Create a temporary directory for cache files
    with tempfile.TemporaryDirectory() as tempdir:

        def add(a: int, b: int) -> int:
            return a + b

        # First call should compute the result and cache it
        result1 = cache(add, cache_folder=tempdir)(1, 2)
        assert result1 == 3

        # Calculate the expected cache key
        expected_cache_key = calculate_cache_key(add, (1, 2), {})
        print(f"Expected cache key: {expected_cache_key}")

        # Check if the cache file is created
        cache_key = f"{expected_cache_key}.pkl"
        cache_file = os.path.join(tempdir, cache_key)
        assert os.path.exists(cache_file)

        # Second call should use the cached result
        with open(cache_file, "rb") as f:
            # Warning: Using pickle can be unsafe with untrusted data.
            cached_result = pickle.load(f)  # Warning: Using pickle can be unsafe with untrusted data. noqa: S301
        result2 = add(1, 2)
        assert result2 == cached_result
