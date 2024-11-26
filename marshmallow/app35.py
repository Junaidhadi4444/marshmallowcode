

from marshmallow import Schema, fields, ValidationError, pre_load

class BandSchema(Schema):
    name = fields.Str()

    @pre_load
    def unwrap_envelope(self, data, **kwargs):
        """Pre-load method to check and extract the 'data' key."""
        if "data" not in data:
            # Raise a ValidationError if 'data' key is not present
            raise ValidationError('Input data must have a "data" key.')
        return data["data"]

# Initialize schema
sch = BandSchema()

# Example input without the 'data' key, which will trigger the ValidationError
try:
    sch.load({"name": "The Band"})  # Missing 'data' envelope
except ValidationError as err:
    print("Validation errors:")
    print(err.messages)  