from marshmallow import Schema, fields, validate


class AdvertisementCreateRequestSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=5, max=100))
    position = fields.String(required=True, validate=validate.Length(min=5, max=100))
    description = fields.String(required=True, validate=validate.Length(min=5, max=100))
