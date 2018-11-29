
from .base_schema import BaseSchema

from marshmallow import fields, validates_schema, ValidationError


class UserSignUpSchema(BaseSchema):

    name = fields.String(required=True, allow_none=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    confirm_password = fields.String(required=True)

    @validates_schema
    def validate_password(self, data):
        if len(data['password'].strip()) < 8:
            raise ValidationError(
                'password must be more than 8 character', 'password')
        elif data['password'] != data['confirm_password']:
            raise ValidationError('password do not match', 'password')
        return True


class UserLoginSchema(BaseSchema):
    username = fields.String()
    email = fields.Email()
    password = fields.String(required=True)

    @validates_schema
    def validate_email_username(self, data):
        if not 'email' in data and 'username' not in data:
            raise ValidationError(
                'must provide either username or email', 'user')
        return True
