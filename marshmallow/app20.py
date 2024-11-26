
#  how to serialize product data with a nested manufacturer field using a different logic,
#  focusing on the relationship between a product and its manufacturer.
from datetime import date
from pprint import pprint
from marshmallow import Schema, fields

# Define the schema for Manufacturer
class ManufacturerSchema(Schema):
    name = fields.Str()
    country = fields.Str()

# Define the schema for Product
class ProductSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    release_date = fields.Date()
    manufacturer = fields.Nested(ManufacturerSchema)

# Example data: Manufacturer and Product
manufacturer = dict(name="Qmobile comp", country="pakistan")
product = dict(name="Qmoblile", price=799.99, release_date=date(2018, 10, 1), manufacturer=manufacturer)

# Create schema instance
schema = ProductSchema()

# Serialize the product data
result = schema.dump(product)

# Pretty print result
pprint(result, indent=2)
