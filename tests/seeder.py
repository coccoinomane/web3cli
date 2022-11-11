"""Please note this file DOES NOT contain tests, but
helper functions to better run tests"""

from typing import Any, Dict, List
from web3cli.helpers.database import db_ready_or_raise
from web3cli.main import Web3Cli
from web3cli.core.models.address import Address
from web3cli.core.models.signer import Signer


def seed_addresses(
    app: Web3Cli, addresses: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Add the given fixture addresses to the database"""
    db_ready_or_raise(app)
    for a in addresses:
        Address.create(
            label=a["label"],
            address=a["address"],
            description=a["description"],
        )
    return addresses


def seed_signers(app: Web3Cli, signers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Add the given fixture signers to the database"""
    db_ready_or_raise(app)
    for s in signers:
        Signer.create_encrypt(label=s["label"], key=s["private_key"], pwd=app.app_key)
    return signers
