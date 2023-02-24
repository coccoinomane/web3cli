"""
PyTest Fixtures.
"""

from typing import Any

import pytest
from cement import fs
from pytest import FixtureRequest

pytest_plugins = [
    "tests.brownie.tests.fixtures",
    "tests.web3cli.fixtures",
    "tests.web3core.fixtures",
]


@pytest.fixture(scope="function")
def tmp(request: FixtureRequest) -> Any:
    """Create a `tmp` object that generates a unique temporary directory, and
    file for each test function that requires it."""
    t = fs.Tmp()
    yield t
    t.remove()


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation: Any) -> None:
    """Reset the local blockchain before each single test.
    https://eth-brownie.readthedocs.io/en/stable/tests-pytest-intro.html"""
    pass
