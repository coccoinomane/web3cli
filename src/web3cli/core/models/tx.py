from __future__ import annotations
from typing import Type
from peewee import TextField, DateTimeField, BigIntegerField
from web3cli.core.exceptions import AddressIsInvalid, TxIsInvalid, TxNotFound
from web3cli.core.models.address import Address
from web3cli.core.models.timestamps_model import TimestampsModel
from playhouse.signals import pre_save
from playhouse.shortcuts import update_model_from_dict
from web3cli.core.models.types import TxFields
from web3cli.core.types import Logger
import re


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
    description = TextField(null=True)
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
        """Create a transaction, or replace it if a tx with the same
        hash already exists, maintaining its ID and relations."""
        tx: Tx = Tx.get_or_none(hash=fields["hash"])
        if tx:
            tx = update_model_from_dict(tx, fields)
            if logger:
                logger(f"Tx {tx.hash} updated")
        else:
            tx = Tx(**fields)
            if logger:
                logger(f"Tx {tx.hash} created")
        tx.save()
        return tx


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
