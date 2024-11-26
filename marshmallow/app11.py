# best practice in post load: Handling Nested Data  
# where the schema handles nested data by converting it into an object.
from marshmallow import Schema, fields, post_load

class Profile():
    def __init__(self, age, address):
        self.age=age
        self.address=address

class ProfileSchema(Schema):
    age=fields.Int(required=True)
    address=fields.Str(required=True)

class User():
    def __init__(self, name, email, profile):
        self.name=name
        self.email=email
        self.profile=profile
        
class UserSchema(Schema):
    name=fields.Str(required=True)
    email=fields.Email(required=True)
    profile=fields.Nested(ProfileSchema)

    @post_load
    def make_user(self, data, **kwargs):
        profile_data=data.pop('profile')
        profile=Profile(**profile_data)
        return User(profile=profile, **data)
    
user_data = {
    "name": "junaid",
    "email": "junaid@gmail.com",
    "profile": {"age": 30, "address": "street 23"}
}
schema=UserSchema()
user=schema.load(user_data)
print(user.name)
print(user.email)
print(user.profile.age)
print(user.profile.address)
