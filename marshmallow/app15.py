# post_dump example1:  

from marshmallow import Schema, fields, post_dump

# User class to represent user data
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

# Schema for User class to handle serialization and validation
class UserSchema(Schema):
    name = fields.Str(required=True) 
    email = fields.Email(required=True)  

    @post_dump
    def add_full_name(self, data, **kwargs):
        """Post-dump method to add a full name field to the serialized output."""
        # data['full_name'] = f"{data['name']} (User)"
        data['full_name'] = "Junaid Ullah" 
        return data

# Example user data
user_data = {
    "name": "junaid",
    "email": "junaid@gmail.com"
}

# Create schema instance
schema = UserSchema()

# Load user data and create User object
user = User(**user_data)

# Serialize (dump) user data
serialized_data = schema.dump(user)  # This should serialize the user object
print(serialized_data)  

