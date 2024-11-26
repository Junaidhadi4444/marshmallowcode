# 
from marshmallow import Schema, fields, pre_load

class MySchema(Schema):
    name = fields.Field()

    @pre_load
    def preprocess(self, data, **kwargs):
        # Ensure step1 is executed before step2
        step1_data = self.step1(data)
        step2_data = self.step2(step1_data)
        return step2_data

    def step1(self, data):
        # Perform the first step of preprocessing
        data['name'] = data['name'].strip()  # Example transformation
        return data

    def step2(self, data):
        # Perform the second step of preprocessing
        data['name'] = data['name'].upper()  # Another transformation
        return data

# Usage example
schema = MySchema()
result = schema.load({"name": "  JUNaid haDi "})
print(result) 
