# two way nesting: 
# Handling Two-Way Nesting in Marshmallow: Serializing Authors and Their Books
# purpose: Avoiding Infinite Recursion, Bidirectional Relationships
from marshmallow import Schema, fields
from pprint import pprint

# Simulated Author class (normally this would come from a database model)
class Author():
    def __init__(self, name):
        self.id=1
        self.name=name
        self.books=[] # Simulated Author class (normally this would come from a database model)


class Book():
    def __init__(self, title, author):
        self.id=101
        self.title=title
        self.author=author
        author.books.append(self) # Add this book to the author's books

# Create an author and a book instance

author=Author(name="josif")
book=Book(title="c++", author=author)


# now define the schemas
class BookSchema(Schema):
    id=fields.Int(dump_only=True)
    title=fields.Str()
    # Use a lambda to avoid circular dependency, and only include specific fields
    author=fields.Nested(lambda: AuthorSchema(only=("id", "name")))

class AuthorSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str()
    # Avoid recursion by excluding the 'author' field in the BookSchema
    books = fields.List(fields.Nested(BookSchema(exclude=("author",))))



print("...............seralaized the book with its author...............")
book_result=BookSchema().dump(book)
pprint(book_result, indent=2)



print("............Serialize the author with their books.............")
author_result=AuthorSchema().dump(author)
pprint(author_result, indent=2)
