# Building Complex Data Structures: Self-Nesting Schemas with Marshmallow

from marshmallow import Schema, fields
from pprint import pprint

# Step 1: Define the User model
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.friends = []  # List of User instances
        self.employer = None  # Reference to another User instance

# Step 2: Define the User Schema
class UserSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    # Nesting the schema within itself to handle relationships
    employer = fields.Nested(lambda: UserSchema(only=("name",)))  # Avoid infinite recursion
    friends = fields.List(fields.Nested(lambda: UserSchema()))  # Self-nested list of friends

# Step 3: Create User Instances and Set Up Relationships
user = User("ihsan", "ihsan@gmail.com")
user.friends.append(User("umar", "umar@gmail.com"))
user.friends.append(User("ali", "ali@gmail.com"))
user.employer = User("khan", "khan@gmail.com")

# Step 4: Serialize the User Data
result = UserSchema().dump(user)

# Step 5: Print the Serialized Result
pprint(result, indent=2)