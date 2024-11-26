# specify a subset of the fields to allow partial loading using dot delimiters.
# purpose: useful for partial updates in web applications
from pprint import pprint
from marshmallow import Schema, fields

# Define User Schema
class UserSchemaStrict(Schema):
    name = fields.String(required=True)
    email = fields.Email()
    created_at = fields.DateTime()

# Define Blog Schema
class BlogSchemaStrict(Schema):
    title = fields.String(required=True)
    author = fields.Nested(UserSchemaStrict, required=True)

# Initialize schema
schema = BlogSchemaStrict()

# Sample data with only some fields provided
author = {"name": "Monty"}
blog = {"title": "Something Completely Different", "author": author}

# Load the blog data with selective validation using dot-delimited paths
result = schema.load(blog, partial=("title", "author.created_at"))

# Pretty print the result
pprint(result)
