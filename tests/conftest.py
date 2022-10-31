"""
PyTest Fixtures.
"""

from typing import Any
from pytest import FixtureRequest
import pytest
from cement import fs


@pytest.fixture(scope="function")
def tmp(request: FixtureRequest) -> Any:
    """
    Create a `tmp` object that geneates a unique temporary directory, and file
    for each test function that requires it.
    """
    t = fs.Tmp()
    yield t
    t.remove()
