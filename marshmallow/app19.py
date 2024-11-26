
# serialization of nested data structures (artist within an album) using the Marshmallow library
from datetime import date
from pprint import pprint
from marshmallow import Schema, fields

class ArtistSchema(Schema):
    name=fields.Str()

class AlbumSchema(Schema):
    title=fields.Str()
    release_date=fields.Date()
    artist=fields.Nested(ArtistSchema())


bowie=dict(name="David bowie")
album=dict(artist=bowie, title="hunky dory", release_date=date(2000, 12, 17))

schema=AlbumSchema()
result=schema.dump(album)
pprint(result, indent=2)


