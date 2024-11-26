# app30books.py
from marshmallow import Schema, fields

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()

    # Reference to AuthorSchema as a string
    author = fields.Nested("AuthorSchema", only=("id", "title"))
