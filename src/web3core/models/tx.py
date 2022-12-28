from __future__ import annotations

import re
from typing import Type

from peewee import BigIntegerField, DateTimeField, TextField
from playhouse.signals import pre_save

from web3core.exceptions import AddressIsInvalid, TxIsInvalid, TxNotFound
from web3core.models.address import Address
from web3core.models.timestamps_model import TimestampsModel
from web3core.models.types import TxFields
from web3core.types import Logger


class Tx(TimestampsModel):
    class Meta:
        table_name = "txs"

    hash = TextField(unique=True)
    chain = TextField()
    to = TextField()
    from_ = TextField(column_name="from")
    value = TextField(null=True)
    gas = BigIntegerField(null=True)
    gas_price = TextField(null=True)
    # timestamp = BigIntegerField(null=True)
    # block = BigIntegerField(null=True)
    desc = TextField(null=True)
    data = TextField(null=True)
    receipt = TextField(null=True)
    created_at = DateTimeField(null=True)
    updated_at = DateTimeField(null=True)

    @classmethod
    def get_by_hash(cls, hash: str) -> Tx:
        """Return the tx object with the given hash, or None if
        it does not exist"""
        return cls.get_or_none(cls.hash == hash)

    @classmethod
    def get_by_hash_or_raise(cls, hash: str) -> Tx:
        """Return the tx object with the given hash; raise
        error if it does not exist"""
        try:
            return cls.get(cls.hash == hash)
        except:
            raise TxNotFound(f"Transaction '{hash}' does not exist")

    @classmethod
    def is_valid_hash(cls, hash: str) -> bool:
        """Is the hash a valid EVM tx hash?"""
        pattern = re.compile(r"^0x[a-fA-F0-9]{64}")
        return bool(re.fullmatch(pattern, hash))

    @classmethod
    def upsert(cls, fields: TxFields, logger: Logger = None) -> Tx:
        """Create tx or update it if one with the same hash already exists"""
        return cls.upsert_by_field(cls.hash, fields["hash"], fields, logger, True)


@pre_save(sender=Tx)
def validate(model_class: Tx, instance: Type[Tx], created: bool) -> None:
    """Validate the transaction which is about to be saved"""
    if not Tx.is_valid_hash(instance.hash):
        raise TxIsInvalid(f"Invalid transaction hash: {instance.hash}")
    if not Address.is_valid_address(instance.from_):
        raise AddressIsInvalid(
            f"Invalid 'from' address for transaction: {instance.from_}"
        )
    if not Address.is_valid_address(instance.to):
        raise AddressIsInvalid(f"Invalid 'to' address for transaction: {instance.to}")
