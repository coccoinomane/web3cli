from __future__ import annotations

from typing import Type

from peewee import TextField
from playhouse.signals import pre_save
from playhouse.sqlite_ext import JSONField
from web3._utils.validation import validate_abi

from web3cli.core.exceptions import ContractIsInvalid, ContractNotFound
from web3cli.core.models.address import Address
from web3cli.core.models.base_model import BaseModel
from web3cli.core.models.types import ContractFields
from web3cli.core.types import Logger


class Contract(BaseModel):
    class Meta:
        table_name = "contracts"

    name = TextField(unique=True)
    desc = TextField(null=True)
    address = TextField()
    chain = TextField()
    abi = JSONField(null=True)

    @classmethod
    def upsert(cls, fields: ContractFields, logger: Logger = None) -> Contract:
        """Create contract or update it if one with the same name already exists"""
        return cls.upsert_by_field(cls.name, fields["name"], fields, logger, True)


@pre_save(sender=Contract)
def validate(model_class: Contract, instance: Type[Contract], created: bool) -> None:
    """Validate the contract which is about to be saved"""
    if not Address.is_valid_address(instance.address):
        raise ContractIsInvalid(
            f"Invalid address given for contract: {instance.address}"
        )
    if instance.abi:
        validate_abi(instance.abi)
