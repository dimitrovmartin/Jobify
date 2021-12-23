from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from models import Positions


class AdvertisementCreateRequestSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=5, max=100))
    position = EnumField(Positions, by_value=True)
    description = fields.String(required=True, validate=validate.Length(min=5, max=100))
    salary = fields.Float(validate=validate.Range(min=650), allow_none=True)


class AdvertisementUpdateRequestSchema(Schema):
    title = fields.String(validate=validate.Length(min=5, max=100), allow_none=True)
    description = fields.String(validate=validate.Length(min=5, max=100), allow_none=True)
    salary = fields.Float(validate=validate.Range(min=650), allow_none=True)
