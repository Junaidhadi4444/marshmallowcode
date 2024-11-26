# pre_load:
from marshmallow import Schema, fields, pre_load

class UserSchema(Schema):
    name = fields.Str()
    slug = fields.Str()

    @pre_load(pass_many=True)
    def slugify_names(self, in_data, many, **kwargs):
        # If 'many' is True, in_data will be a list of items
        if many:
            for item in in_data:
                item["slug"] = item["name"].lower().strip().replace(" ", "-")
            return in_data
        else:
            # Handle single item
            in_data["slug"] = in_data["name"].lower().strip().replace(" ", "-")
            return in_data

# Example usage with a single user
single_user_data = {"name": "junaid hadi"}
single_user_schema = UserSchema()
single_user_result = single_user_schema.load(single_user_data)
print(single_user_result)


# Example usage with multiple users
multiple_users_data = [{"name": "junaid hadi"}, {"name": "umar ali"}]
multiple_user_result = single_user_schema.load(multiple_users_data, many=True)
print(multiple_user_result)