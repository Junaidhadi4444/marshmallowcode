# app30authors.py
from marshmallow import Schema, fields

class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()

    # Reference to BookSchema as a string
    books = fields.List(fields.Nested("BookSchema", exclude=("author",)))




