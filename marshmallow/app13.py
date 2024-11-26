# pre_load example#1
# "Preprocessing Input Data Using @pre_load in Marshmallow"
# using strip for name and lower and strip for
from marshmallow import Schema, fields, pre_load

class User():
    def __init__(self, name, email):
        self.name=name
        self.email=email

    def __repr__(self):
        return f" user (name={self.name}, email={self.email})"
# user schema
class UserSchema(Schema):
    name=fields.Str(required=True)
    email=fields.Email(required=True)

    @pre_load
    def preprocess_data(self, data, **kwargs):
        data["name"]=data["name"].strip()
        data["email"]=data["email"].lower().strip()
        return data
user_data={
    "name":"  junadid",
    "email": " Junaid@gmail.COM  "
}

schema=UserSchema()
user=schema.load(user_data)
print(user)