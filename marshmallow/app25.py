# use of dotted paths with the only argument in Marshmallow to specify which fields to serialize from nested objects.
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

# Site class definition
class Site:
    def __init__(self, blog):
        self.blog = blog  # A Blog object

# Define UserSchema
class UserSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime()

# Define BlogSchema2 with specific fields using 'only'
class BlogSchema2(Schema):
    title = fields.String(required=True)
    author = fields.Nested(UserSchema(only=("name",)))  # Only serialize the email field

# Define SiteSchema with nested BlogSchema2
class SiteSchema(Schema):
    blog = fields.Nested(BlogSchema2)

# Create User, Blog, and Site instances
user = User(name="Monty", email="monty@python.org")
blog = Blog(title="Something Completely Different", author=user)
site = Site(blog=blog)

# Serialize the Site instance, only including the specified fields
schema = SiteSchema(only=("blog.author.name",))  # We want to include only the author's email
result = schema.dump(site)

# Pretty print the serialized result
pprint(result)