# using pre_post example2:
# Deserializing User Data with Marshmallow: Single and Multiple User Handling

from marshmallow import Schema, fields, pre_load
# user class
class User():
    def __init__(self, name, email):
        self.name=name
        self.email=email

    def __repr__(self):
        return f"user(name={self.name}, email={self.email})"
    
# schema for user class
class UserSchema(Schema):
    name=fields.Str(required=True)
    email=fields.Email(required=True)

    @pre_load(pass_many=True)
    def remove_envelope(self, data, many, **kwargs):
        namespace="results" if many else "result"
        return data[namespace]
    
# ex with single user
single_user_data={
    "result":{
        "name":"junaid",
        "email":"junaid@gamil.com"
    }
}


multi_user_data = {
    "results": [
        {
            "name": "junaid",  
            "email": "junaid@gmail.com"  
        },
        {
            "name": "izhar", 
            "email": "izhar@gmail.com"
        }
    ]
}
schema=UserSchema()
# load single user data
user_dic_single=schema.load(single_user_data)
print("......this is for single user.........")
print(user_dic_single)

# load multiple user data
user_dict_multi = schema.load(multi_user_data, many=True)
# Create User objects
users_multiple = [User(**user_dict) for user_dict in user_dict_multi]  # Create User objects
print("........this is for multiple user..........")
print(users_multiple)