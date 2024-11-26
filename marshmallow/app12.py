# Example with @post_load for lowerstrip_email
from marshmallow import Schema, fields, post_load

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

# Define the User schema
class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)

    # Modify email to be lowercase and stripped of any extra spaces after deserialization
    @post_load
    def lowerstrip_email(self, item, many, **kwargs):
        item["email"] = item["email"].lower().strip()
        return item

    # Optional: You can also add a @post_load method to create a User object from the data
    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

# Example usage
user_data = {
    "name": "Junaid",
    "email": "junaid@gmail.com"  # Extra spaces and mixed case
}

schema = UserSchema()
user = schema.load(user_data)

# Accessing the attributes after deserialization
print(user.name)   
print(user.email)  
