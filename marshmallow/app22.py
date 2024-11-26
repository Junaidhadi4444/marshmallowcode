# Serializing Blog Authors with Nested User Schemas in Marshmallow
from marshmallow import Schema, fields
from  pprint import pprint
import datetime as dt

class User:
    def __init__(self, name, email):
        self.name=name
        self.email=email
        self.created_at=dt.datetime.now()
        self.friends=[]
        self.employer = None


class Blog():
    def __init__(self, title, auther):
        self.title=title
        self.auther=auther

class UserSchema(Schema):
    name=fields.String(required=True)
    email=fields.Email(required=True)
    created_at=fields.DateTime()

class BlogSchema(Schema):
    title=fields.String()
    auther=fields.Nested(UserSchema)

user = User(name="ali", email="ali@gmail.com")

# Create a Blog instance with the User as the author
blog = Blog(title="Something Completely Different", auther=user)

# Serialize the Blog instance
result = BlogSchema().dump(blog)

# Pretty print the serialized result
pprint(result)
         