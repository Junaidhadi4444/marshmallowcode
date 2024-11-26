# pre_dump example1:
# Pre-Dump Data Modification: Adding Prefix to User Name Before Serialization
from marshmallow import Schema, fields, pre_dump

class User():
    def __init__(self, name, email, age):
        self.name=name
        self.email=email
        self.age=age

    def __repr__(self):
        return f"user(name={self.name}, name={self.email}, age={self.age})"

class UserSchema(Schema):
    name=fields.Str(required=True)
    email=fields.Email(required=True)
    age=fields.Int(required=True)

    @pre_dump
    def modify_data(self, user, **kwargs):
        user.name=f"this mr {user.name}"
        return user
    
def serialize_user(user_data):
    """Function to serialize user data."""
    schema = UserSchema()  # Create schema instance
    # Serialize the user data
    serialized_data = schema.dump(User(**user_data))
    return serialized_data

user_data = {
    "name": "junaid",
    "email": "junaid@gmail.com",
    "age": 30
}
print("Serialized User Data:")
print(serialize_user(user_data))