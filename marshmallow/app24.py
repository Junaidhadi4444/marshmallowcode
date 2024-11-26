# specifying Nested Fields in Marshmallow Using the only Argument
# purpose: 1) Limit Output Data 2) Improve Performance 3) 
from marshmallow import Schema, fields, pprint
import datetime as dt

# User class definition
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

# Blog class definition
class Blog:
    def __init__(self, title, author):
        self.title = title
        self.author = author  # A User object

# UserSchema definition
class UserSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime()

class BlogSchema(Schema):
    title=fields.String(required=True)
    author=fields.Nested(UserSchema(only=("email",)))


author = User(name="Monty", email="monty@gmail.com")

# Create a Blog instance with the User as the author
blog = Blog(title="Something Completely Different", author=author)

# Serialize the Blog instance using BlogSchema2
schema = BlogSchema()
result = schema.dump(blog)

pprint(result)