from datetime import datetime
from enum import IntEnum
from tortoise import fields
from tortoise_api_model import Model


class UserStatus(IntEnum):
    kicked = 0
    member = 1
    administrator = 2


class User(Model):
    id: str = fields.BigIntField(pk=True)
    name: str = fields.CharField(63)
    status: UserStatus = fields.IntEnumField(UserStatus, default=UserStatus.member)
    referrer: fields.ForeignKeyNullableRelation["User"] = fields.ForeignKeyField("models.User", related_name="referrals", null=True)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)

    referrals: fields.BackwardFKRelation["User"]

    class Meta:
        table_description = "Bot users"
