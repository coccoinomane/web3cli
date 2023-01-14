"""
PyTest Fixtures.
"""

from typing import Any

import pytest
from cement import fs
from pytest import FixtureRequest

pytest_plugins = [
    "tests.brownie.fixtures",
    "tests.web3cli.fixtures",
    "tests.web3core.fixtures",
]


@pytest.fixture(scope="function")
def tmp(request: FixtureRequest) -> Any:
    """Create a `tmp` object that geneates a unique temporary directory, and
    file for each test function that requires it."""
    t = fs.Tmp()
    yield t
    t.remove()
