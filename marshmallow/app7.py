# how vaidation workin marshmalow 
# custom validation function 
from marshmallow import Schema, fields, post_load, ValidationError, validates

class Person:
    def __init__(self, name, age, email):
        self.name=name
        self.age=age
        self.email=email
        
    def __repr__(self):
        return f'{self.name} is {self.age} year old.'
    
# creating schema 
class PersonSchema(Schema):
    name=fields.String()
    age=fields.Integer()
    email=fields.Email()
    # using required but i dont update the class to used this
    location=fields.String( required=True)

    # validate decorator 
    @validates('age')
    def validate_age(self, age):
        if age <=0:
            raise ValidationError('the age should not be zero or negative')
            #return False

    # using post_load decorator 
    @post_load
    def creat_person(self, data, **kwargs):
        return Person(**data)

# get the input from the user 
input_data={}
input_data['name']=input('what is your name?')
input_data['age']=input('what is your age?')
input_data['email']=input('what is your email?')


try:
    schema=PersonSchema()
    Person=schema.load(input_data)
    print(Person)

except ValidationError as err:
    print(err)
    print(err.valid_data)