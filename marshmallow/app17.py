# nested schema example1:
# Implementing Nested Schemas: Serializing and Deserializing User Data with Address Objects
#  Serializing and Deserializing Complex Objects in Marshmallow

from marshmallow import Schema, fields

class Address():
    def __init__(self, street, city, state, zip_code ):
        self.street=street
        self.city=city
        self.state=state
        self.zip_code=zip_code
    def __repr__(self):
        return f"Address(street={self.street}, city={self.city}, state={self.state}, zip_code={self.zip_code})"

class User:
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address  # Address is an object, not just a string

    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, address={self.address})"

class AddressSchema(Schema):
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    zip_code = fields.Str(required=True)

# Define the User schema with a nested Address schema
class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    # Use Nested field for the address, linking it to AddressSchema
    address = fields.Nested(AddressSchema)

address_data = {
    "street": "123",
    "city": "xyz",
    "state": "abc",
    "zip_code": "2334"
}

# Example user data with nested address
user_data = {
    "name": "Junaid Ullah",
    "email": "junaid@example.com",
    "address": address_data
}

# create schema instances for both
address_schema=AddressSchema()
user_schema=UserSchema()

# Serialize user data (converting objects to dictionaries)
serialized_user = user_schema.dump(User(**user_data))
print("Serialized User Data with Nested Address:")
print(serialized_user)

# Deserialize user data (converting dictionaries to objects)
deserialized_user = user_schema.load(user_data)
print("\nDeserialized User Data:")
print(deserialized_user)