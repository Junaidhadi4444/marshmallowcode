# Enhancing User Objects with Default Status During Deserialization Using Marshmallow's @post_load
# edit data after decentraliztion 
from  marshmallow import Schema, fields, post_load
class User:
    def __init__(self, name, email, status):
        self.name = name
        self.email = email
        self.status = status

class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)

    @post_load
    def add_status(self, data, **kwargs):
        data["status"] = "active"  # Add default status
        return User(**data)

# Usage
user_data = {"name": "junaid", "email": "junaid@gmail.com"}
schema = UserSchema()
user = schema.load(user_data)
print(user.status)  
