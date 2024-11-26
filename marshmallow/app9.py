# post_load example
# Transforming Deserialized Data into Python Objects with Marshmallow's @post_load
from marshmallow import Schema, fields, post_load

# Define a class
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# Define a schema
class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)

    # Method that will run after deserialization
    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

# Example usage
user_data = {"name": "junaid", "email": "junaid@gmail.com"}
schema = UserSchema()

# Deserializing into a User object
user = schema.load(user_data)
print(user.name)
print(user.email)  
