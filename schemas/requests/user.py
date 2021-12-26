from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from models import Positions


class BaseUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=255))


class ApplicantRegisterRequestSchema(BaseUserSchema):
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    position = EnumField(Positions, by_value=True)
    education = fields.String(required=True, validate=validate.Length(min=10, max=255))
    phone = fields.String(required=True, validate=validate.Length(min=10, max=10))
    photo = fields.String(required=True)
    photo_extension = fields.String(required=True)


class ApplicantLoginRequestSchema(BaseUserSchema):
    pass


class CompanyRegisterRequestSchema(BaseUserSchema):
    company_name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    address = fields.String(required=True, validate=validate.Length(min=2, max=255))
    employees_count = fields.Integer(required=True)
    description = fields.String(required=True, validate=validate.Length(min=10, max=255))
    phone = fields.String(required=True, validate=validate.Length(min=10, max=10))


class CompanyLoginRequestSchema(BaseUserSchema):
    pass


class AdminRegisterRequestSchema(BaseUserSchema):
    phone = fields.String(required=True, validate=validate.Length(min=10, max=10))


class AdminLoginRequestSchema(BaseUserSchema):
    pass