import datetime as dt
from typing import Type
from playhouse.signals import pre_save
from web3cli.core.models.base_model import BaseModel


class TimestampsModel(BaseModel):
    """Extend this class to automatically populate the 'created_at'
    and 'updated_at' timestamps each time a record is created
    or updated."""

    def created_at_short(self) -> str:
        """Creation timestamp in short form"""
        return self.created_at.strftime("%Y%b%d_%H:%M:%S")

    def updated_at_short(self) -> str:
        """Update timestamp in short form"""
        return self.updated_at.strftime("%Y%b%d_%H:%M:%S")


def timezone_now() -> dt.datetime:
    """Like now but with timezone information"""
    return dt.datetime.now(dt.timezone.utc).astimezone()


@pre_save(sender=TimestampsModel)
def add_timestamps(
    model_class: TimestampsModel, instance: Type[TimestampsModel], created: bool
) -> None:
    if created == True:
        instance.created_at = timezone_now()
    instance.updated_at = timezone_now()