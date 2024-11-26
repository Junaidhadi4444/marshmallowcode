

from marshmallow import Schema, fields, ValidationError, pre_load

class BandSchema(Schema):
    name=fields.Str()

    @pre_load
    def unwrape_envelope(self, data, **kwargs):
        if "data" not in data:
            raise ValidationError(
                'input must have a "data" key.', "preprossing"   # custom error key
            )
        return data["data"]
    
schema=BandSchema()

try:
    schema.load({"name":"the bond"})
except ValidationError as err:
    print(err.messages)

'''
# this is correct data
valid_data = {"data": {"name": "The Band"}}

# Load and validate the correct data
try:
    result = schema.load(valid_data)
    print("Loaded data:", result)
except ValidationError as err:
    print("Validation errors:", err.messages)
'''