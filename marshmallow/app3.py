# schema 
# using post_load decorator 
# using dump
from marshmallow import Schema, fields, post_load
class Person:
    def __init__(self, age, name):
        self.name=name
        self.age=age
        
    def __repr__(self):
        return f'{self.name} is {self.age} year old.'
    
# creating schema 
class PersonSchema(Schema):
    name=fields.String()
    age=fields.Integer()

    # using post_load decorator 
    @post_load
    def creat_person(self, data, **kwargs):
        return Person(**data)

# get the unput from the user 
input_data={}
input_data['name']=input('what is your name?')
input_data['age']=input('what is your age?')

# instanciate the schema
schema=PersonSchema()
result=schema.dump(input_data)

print(result)

