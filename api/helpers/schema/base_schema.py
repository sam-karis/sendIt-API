
from marshmallow import Schema, fields, ValidationError


class BaseSchema(Schema):

    def load_json_data(self, json_data):
        try:
            result = self.load(json_data)
        except ValidationError as err:
            raise ValidationError(err, data=err.messages)

        return result
