from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from models import Positions


class AdvertisementCreateRequestSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=5, max=100))
    position = EnumField(Positions, by_value=True)
    description = fields.String(required=True, validate=validate.Length(min=5, max=100))


class AdvertisementUpdateRequestSchema(Schema):
    title = fields.String(required=False)
    position = EnumField(Positions, by_value=True)
    description = fields.String(required=False)
    salary = fields.Float(required=False)
