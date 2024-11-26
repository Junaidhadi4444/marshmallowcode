# Validating Usernames with Custom Constraints in Marshmallow

from marshmallow import Schema, fields, validates, ValidationError
import re

class UserSchema(Schema):
    username = fields.Str(required=True)

    # Define the reserved words
    reserved_words = ['admin', 'root', 'superuser', 'testuser']

    @validates('username')  # Corrected: use quotes for field name
    def validate_username(self, value):
        # Length validation
        if len(value) < 3 or len(value) > 20:
            raise ValidationError('Username must be between 3 and 20 characters long.')

        # No leading/trailing whitespace
        if value != value.strip():
            raise ValidationError('Username cannot have leading or trailing spaces.')

        # No repeated characters (3 or more)
        if re.search(r'(.)\1{2,}', value):
            raise ValidationError('Username cannot contain repeated characters.')

        # No sequential characters (4 or more)
        if re.search(r'1234|abcd|ijkl|mnop|qrst|wxyz', value):
            raise ValidationError('Username cannot contain sequential characters.')

        # No numeric-only usernames
        if value.isdigit():
            raise ValidationError('Username cannot be only numbers.')

        # No consecutive underscores
        if '__' in value:
            raise ValidationError('Username cannot contain consecutive underscores.')

        # Starts/ends with letter
        if not (value[0].isalpha() and value[-1].isalpha()):
            raise ValidationError('Username must start and end with a letter.')

# Function to validate user input
def validate_username_ex(username):
    schema = UserSchema()
    try:
        schema.load({'username': username})
        print(f"'{username}' is a valid username.")
    except ValidationError as err:
        print(f"Validation errors for '{username}': {err.messages}")

# Main program to get input from the user
def main():
    username = input("Enter your name: ")
    validate_username_ex(username)

if __name__ == "__main__":
    main()
