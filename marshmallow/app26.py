# Extracting Specific Fields from Nested Objects Using the Pluck Field
from marshmallow import Schema, fields
from pprint import pprint

class User:
    def __init__(self, name, email, friends=None):
        self.name = name
        self.email = email
        self.friends = friends if friends else []

# Define the schema
class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    friends = fields.Pluck("self", "name", many=True)

# Create user instances
user1 = User(name="junaid", email="junaid@gmail.com", friends=[])
user2 = User(name="fawad", email="fawad@gmail.com")
user3 = User(name="umar", email="umar@gmail.com")
user1.friends = [user2, user3]

# Serialize the data
serialized_data = UserSchema().dump(user1)
pprint(serialized_data)

pprint(".....................")
# Deserialize the data
deserialized_data = UserSchema().load(serialized_data)
pprint(deserialized_data)
