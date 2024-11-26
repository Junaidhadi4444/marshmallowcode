# pre_load, post_load, post_dump
# Utilizing Enveloping in Marshmallow Schemas for Data Organization
#
from marshmallow import Schema, fields, pre_load, post_load, post_dump

class User():
    def __init__(self, name, email):
        self.name=name
        self.email=email

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"
    
class BaseSchema(Schema):
    __envelope__ = {"single": None, "many": None}
    __model__=User
    def get_envelope_key(self, many):
        # Helper to get the envelope key.
        key=self.__envelope__["many"] if many else self.__envelope__["single"]
        assert key is not None, "Envelope key is undefined"
        return key
    
    @pre_load(pass_many=True)
    def unwrape_envelope(self, data, many, **kwargs):
        key=self.get_envelope_key(many)
        return data[key]
    
    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many, **kwargs):
        # Wraps data in the envelope.
        key = self.get_envelope_key(many)
        return {key: data}
    
    @post_load
    def make_object(self, data, **kwargs):
        """Creates a User object from the data."""
        return self.__model__(**data)
    

class UserSchema(BaseSchema):
    __envelope__={"single":"user", "many":"users"}
    __model__=User
    name=fields.Str(required=True)
    email=fields.Email(required=True)

userschema=UserSchema()

user = User("umar", email="umar@gmail.com")
user_data=userschema.dump(user)
print("Serialized single user data:")
print(user_data)

users = [
    User("umar", email="umar@gmail.com"),
    User("khan", email="khan@gmail.com"),
]
users_data = userschema.dump(users, many=True)
print("\nSerialized multiple users data:")
print(users_data)

user_objs = userschema.load(users_data, many=True)
print("\nDeserialized user objects:")
print(user_objs)