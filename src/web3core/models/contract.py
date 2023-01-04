from __future__ import annotations

from typing import Type

from peewee import TextField
from playhouse.signals import pre_save
from playhouse.sqlite_ext import JSONField
from web3._utils.validation import validate_abi

from web3core.exceptions import ContractIsInvalid, ContractNotFound
from web3core.models.address import Address
from web3core.models.base_model import BaseModel
from web3core.models.types import ContractFields
from web3core.types import Logger


class Contract(BaseModel):
    class Meta:
        table_name = "contracts"
        indexes = ((("name", "chain"), True),)  # name and chain must be unique together

    name = TextField()
    desc = TextField(null=True)
    type = TextField(null=True)
    address = TextField()
    chain = TextField()
    abi = JSONField(null=True)

    @classmethod
    def get_by_name_and_chain(cls, name: str, chain: str) -> Contract:
        """Return the contract with the given name on the given chain,
        or None if it does not exist"""
        return cls.get_or_none((cls.name == name) & (cls.chain == chain))

    @classmethod
    def get_by_name_and_chain_or_raise(cls, name: str, chain: str) -> Contract:
        """Return the contract with the given name on the given chain,
        or raise if it does not exist"""
        try:
            return cls.get((cls.name == name) & (cls.chain == chain))
        except cls.DoesNotExist:
            raise ContractNotFound(
                f"Contract '{name}' on chain '{chain}' does not exist"
            )

    @classmethod
    def upsert(cls, fields: ContractFields, logger: Logger = None) -> Contract:
        """Create contract or update it if one with the same name already exists"""
        return cls.upsert_by_query(
            (cls.name == fields["name"]) & (cls.chain == fields["chain"]),
            fields,
            logger,
            True,
        )


@pre_save(sender=Contract)
def validate(model_class: Contract, instance: Type[Contract], created: bool) -> None:
    """Validate the contract which is about to be saved"""
    if not Address.is_valid_address(instance.address):
        raise ContractIsInvalid(
            f"Invalid address given for contract: {instance.address}"
        )
    if instance.abi:
        validate_abi(instance.abi)


@pre_save(sender=Contract)
def sanitize(model_class: Contract, instance: Type[Contract], created: bool) -> None:
    """Sanitize the contract which is about to be saved"""
    instance.name = instance.name.lower()
