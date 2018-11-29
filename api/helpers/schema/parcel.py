
from .base_schema import BaseSchema

from marshmallow import fields, validates_schema, ValidationError


class CreateSchema(BaseSchema):

    title = fields.String(required=True, allow_none=False)
    destination = fields.String(required=True)
    quantity = fields.String(required=True)


class DestinationSchema(BaseSchema):

    destination = fields.String(required=True, allow_none=False)

    @validates_schema
    def remove_whiteSpace(self, data):
        if len(data['destination'].strip()) < 1:
            raise ValidationError(
                'Destination cannot be empty', 'destination')
        return True


class StatusSchema(BaseSchema):

    status = fields.String(required=True, allow_none=False)

    @validates_schema
    def remove_whiteSpace(self, data):
        allowed_status = ('Pending', 'In-transit', 'Delivered')
        if len(data['status'].strip()) < 1:
            raise ValidationError(
                'Status cannot be empty', 'status')
        if data['status'].capitalize() not in allowed_status:
            raise ValidationError(
                f'Status can only be {allowed_status}', 'status')
        return True


class PresentLocationSchema(BaseSchema):

    current_location = fields.String(required=True, allow_none=False)
