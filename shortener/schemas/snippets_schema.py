import datetime

from marshmallow_jsonapi import fields

from shortener.schemas.base import BaseSchema


def get_time_since_creation(record):
    time_diff = datetime.datetime.now() - record.created_at
    return str(time_diff)


class SnippetsSchema(BaseSchema):

    id = fields.UUID(dump_only=True)
    desktop_redirect = fields.Url(required=True)
    desktop_redirect_count = fields.Integer(dump_only=True)
    mobile_redirect = fields.Url()
    mobile_redirect_count = fields.Integer(dump_only=True)
    tablet_redirect = fields.Url()
    tablet_redirect_count = fields.Integer(dump_only=True)
    short_url = fields.Url()
    time_since_creation = fields.Function(
        lambda obj: get_time_since_creation(obj),
        dump_only=True,
    )

    class Meta:
        type_ = 'snippets'
        strict = True
