"""
PyTest Fixtures.
"""

from typing import Any, List, Dict
from pytest import FixtureRequest
import pytest
from cement import fs


@pytest.fixture()
def addresses() -> List[Dict[str, Any]]:
    return [
        {
            "label": "Ethereum foundation",
            "address": "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
        },
        {
            "label": "Binance hot wallet",
            "address": "0x8894e0a0c962cb723c1976a4421c95949be2d4e3",
        },
    ]


@pytest.fixture(scope="function")
def tmp(request: FixtureRequest) -> Any:
    """
    Create a `tmp` object that geneates a unique temporary directory, and file
    for each test function that requires it.
    """
    t = fs.Tmp()
    yield t
    t.remove()
