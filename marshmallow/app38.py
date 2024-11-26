from marshmallow import Schema, fields, validates_schema, ValidationError

class NumberSchema(Schema):
    field_a=fields.Integer(required=True)
    field_b=fields.Integer(required=True)


    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if data['field_b']>=data['field_a']:
            raise ValidationError(" fielld a must be grater then field b")
    

schema = NumberSchema()

# Example 1: Valid input
try:
    result = schema.load({"field_a": 10, "field_b": 2})
    print("Valid input:", result)  
except ValidationError as err:
    print(err.messages)
