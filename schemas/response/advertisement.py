from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models import Positions


class AdvertisementResponseSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)
    position = EnumField(Positions, by_value=True)
    salary = fields.Float(required=True)
    description = fields.String(required=True)
