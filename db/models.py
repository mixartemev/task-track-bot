from datetime import datetime, timedelta, date
from enum import IntEnum
from typing import Type

from tortoise import fields
from tortoise.signals import post_save
from tortoise_api_model import Model


class UserStatus(IntEnum):
    kicked = 0
    member = 1
    administrator = 2

class TaskStatus(IntEnum):
    deleted = 0
    active = 1
    paused = 2
    done = 3


class User(Model):
    id: int = fields.BigIntField(True)
    name: str = fields.CharField(63)
    status: UserStatus = fields.IntEnumField(UserStatus, default=UserStatus.member)
    referrer: fields.ForeignKeyNullableRelation["User"] = fields.ForeignKeyField("models.User", related_name="referrals", null=True)
    referrer_id: int
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)

    referrals: fields.BackwardFKRelation["User"]
    my_tasks: fields.BackwardFKRelation["Task"]
    created_tasks: fields.BackwardFKRelation["Task"]

    class Meta:
        table_description = "Bot users"


class Task(Model):
    id: int
    name: str = fields.CharField(255)
    body: str = fields.CharField(4095)
    status: TaskStatus = fields.IntEnumField(TaskStatus, default=TaskStatus.active)
    doer: fields.ForeignKeyNullableRelation[User] = fields.ForeignKeyField("models.User", related_name="my_tasks", null=True)
    doer_id: int
    creator: fields.ForeignKeyNullableRelation[User] = fields.ForeignKeyField("models.User", related_name="created_tasks")
    creator_id: int
    deadline: date = fields.DateField(null=True)
    parent: fields.ForeignKeyNullableRelation["Task"] = fields.ForeignKeyField("models.Task", related_name="subtasks", null=True)
    parent_id: int
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)

    subtasks: fields.BackwardFKRelation["Task"]

    class Meta:
        unique_together = 'name', 'creator'
        table_description = "Tasks"

@post_save(Task)
async def task_doer_set(
    sender: Type[Task], instance: Task, created: bool, using_db, update_fields
) -> None:
    if created:
        instance.doer_id = instance.doer_id or instance.creator_id
        await instance.save()
