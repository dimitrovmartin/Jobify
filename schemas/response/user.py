from marshmallow import fields, Schema
from marshmallow_enum import EnumField

from models import Positions


class ApplicantResponseSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    position = EnumField(Positions, by_value=True)
    education = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.Email(required=True)
    photo_url = fields.String(required=True)
