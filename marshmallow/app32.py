# post load:
# Data Transformation Post-load Methods

from marshmallow import Schema, fields, post_load

class UserSchema(Schema):
    name = fields.Str()
    slug = fields.Str()

    @post_load
    def slugify_name(self, in_data, **kwargs):
        # Convert slug to lowercase and replace spaces with hyphens
        in_data["slug"] = in_data["slug"].lower().strip().replace(" ", "-")
        return in_data

# Initialize schema
schema = UserSchema()

# Load input data
result = schema.load({"name": "Ste ve", "slug": "Steve Loria "})
print(result)
# Access the slug field
print(result["slug"])  # Output: 'steve-loria'
