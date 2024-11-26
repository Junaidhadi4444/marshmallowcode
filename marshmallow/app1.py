# marshmallow
# used class directly heare


class Person:
    def __init__(self, age, name):
        self.name=name
        self.age=age
        
    def __repr__(self):
        return f'{self.name} is {self.age} year old.'
# get the input from the user 
input_data={}
input_data['name']=input('what is your name?')
input_data['age']=input('what is your age?')

person=Person(name=input_data['name'], age=input_data['age'])
print(person)

