from datetime import datetime, timezone

from peewee import BigIntegerField, CharField, BooleanField, DateTimeField, FloatField

from .base import BaseModel


class User(BaseModel):
    BACHELOR = 'bachelor'

    id = BigIntegerField(primary_key=True)
    name = CharField(default=None)
    username = CharField(default=None, null=True)
    language = CharField(default='en')

    is_admin = BooleanField(default=False)
    is_ordered_call = BooleanField(default=False)
    phone = CharField(default=None, null=True)
    score_126 = FloatField(default=None, null=True)
    score_172 = FloatField(default=None, null=True)
    score_for = CharField(default=None, null=True)

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc), null=True)

    class Meta:
        table_name = 'users'
