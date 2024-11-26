# Handling Partial Data Validation with Marshmallow's partial=True Feature
# purpose Flexibility, Ease of Updates
from pprint import pprint
from marshmallow import Schema, fields

# Define User Schema
class UserSchemaStrict(Schema):
    name = fields.String(required=True)
    email = fields.Email()
    created_at = fields.DateTime(required=True)

# Define Blog Schema
class BlogSchemaStrict(Schema):
    title = fields.String(required=True)
    author = fields.Nested(UserSchemaStrict, required=True)

# Initialize schema
schema = BlogSchemaStrict()

# Sample blog data with an empty author
blog = {
    "title": "Something Completely Different",
    "author": {}  # No user information provided
}

# Load the blog data partially
result = schema.load(blog, partial=True)


pprint(result)