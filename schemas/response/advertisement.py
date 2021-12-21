from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from models import Positions


class AdvertisementResponseSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True, validate=validate.Length(min=5, max=100))
    position = EnumField(Positions, by_value=True)
    salary = fields.Float(required=False)
    description = fields.String(required=True, validate=validate.Length(min=5, max=100))
