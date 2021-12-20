from marshmallow import Schema, fields, validate


class AdvertisementCreateRequestSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=5, max=100))
    position = fields.String(required=True, validate=validate.Length(min=5, max=100))
    description = fields.String(required=True, validate=validate.Length(min=5, max=100))


class ApplyAdvertisementRequestSchema(Schema):
    id = fields.Integer(required=True)


class AdvertisementUpdateRequestSchema(Schema):
    title = fields.String(required=False)
    position = fields.String(required=False)
    description = fields.String(required=False)
    salary = fields.Float(required=False)
