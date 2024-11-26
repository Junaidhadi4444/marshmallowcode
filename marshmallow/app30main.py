# pass a class name as a string to Nested. This is useful for avoiding circular imports
#  when your schemas are located in different modules
# purpose: Enhancing Code Organization, Avoiding Infinite Recursion
from pprint import pprint

from app30authors import AuthorSchema
from app30books import BookSchema

author_data = {"id": 1, "title": "David"}
book_data = {"id": 1, "title": "Flask", "author": author_data}

print("........Serialize the book data...........")
book_schema = BookSchema()
book_result = book_schema.dump(book_data)
pprint(book_result)

print("............Serialize the author data............")
author_schema = AuthorSchema()
author_result = author_schema.dump(author_data)
pprint(author_result)
