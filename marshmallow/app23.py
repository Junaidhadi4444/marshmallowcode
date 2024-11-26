# Using Marshmallow for Serializing Blogs with Multiple Collaborators
from marshmallow import Schema, fields
from pprint import pprint
from datetime import date
import datetime as dt 

class User():
    def __init__(self, name, email):
        self.name =name
        self.email=email
        self.created_at=dt.datetime.now()

class Blog():
    def __init__(self, title, collaborators):
        self.title=title
        self.collaborators=collaborators  # list of user objects


class UserSchema(Schema):
    name=fields.String(required=True)
    email=fields.Email(required=True)
    created_at=fields.DateTime()


class BlogSchema(Schema):
    title=fields.String(required=True)
    collaborators = fields.List(fields.Nested(UserSchema), required=True)

user1 = User(name="Ali", email="ali@gmail.com")
user2 = User(name="Sara", email="sara@gmail.com")
user3 = User(name="John", email="john@example.com")

blog = Blog(title="Collaborative Writing", collaborators=[user1, user2, user3])

result=BlogSchema().dump(blog)

pprint(result)