from __future__ import annotations

from typing import Any, Dict, List, Type, TypeVar

from peewee import Field, SqliteDatabase
from playhouse.shortcuts import update_model_from_dict
from playhouse.signals import Model

from web3cli.core.exceptions import RecordNotFound
from web3cli.core.types import Logger

db = SqliteDatabase(None, pragmas={"foreign_keys": 1})
"""Database, initialized during post_setup hook"""

Self = TypeVar("Self", bound="BaseModel")
"""Type for class methods returning (sub)class instances"""


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get_all_as_dicts(cls, order_by: Any = None) -> List[Dict[str, Any]]:
        query = cls.select()
        if order_by:
            query = query.order_by(order_by)
        return [m for m in query.dicts()]

    @classmethod
    def get_all(cls: Type[Self], order_by: Any = None) -> List[Self]:
        query = cls.select()
        if order_by:
            query = query.order_by(order_by)
        return [m for m in query]

    @classmethod
    def get_by_name(cls: Type[Self], name: str) -> Self:
        """Return the record with the given name, or None if
        it does not exist"""
        return cls.get_or_none(cls.name == name)

    @classmethod
    def get_by_name_or_raise(cls: Type[Self], name: str) -> Self:
        """Return the record with the given name; raise
        error if it does not exist"""
        try:
            return cls.get(cls.name == name)
        except cls.DoesNotExist:
            raise RecordNotFound(f"{cls.__name__} '{name}' does not exist")

    @classmethod
    def upsert_by_field(
        cls: Type[Self],
        field: Field,
        value: Any,
        fields: Any,
        logger: Logger = None,
        ignore_unknown: bool = True,
    ) -> Self:
        """Create a new record, or update it if a record already exists
        that matches the given query (field=value)."""
        instance: Self = cls.get_or_none(field == value)
        if instance:
            instance = update_model_from_dict(
                instance, fields, ignore_unknown=ignore_unknown
            )
            instance.save()
            if logger:
                logger(f"{cls.__name__} {getattr(instance, field.name)} updated")
        else:
            instance = cls(**fields)
            instance.save()
            if logger:
                logger(f"{cls.__name__} {getattr(instance, field.name)} created")
        return instance
