from marshmallow import Schema, fields, validate


class AdvertisementResponseSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True, validate=validate.Length(min=5, max=100))
    position = fields.String(required=True, validate=validate.Length(min=5, max=100))
    salary = fields.Float(required=False)
    description = fields.String(required=True, validate=validate.Length(min=5, max=100))