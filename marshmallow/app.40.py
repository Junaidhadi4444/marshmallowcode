
# hostel managment 

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, validate, post_load, ValidationError
from sqlalchemy.exc import IntegrityError
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/hostel_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# create models for student, room, booking  entity
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=True)
    
    student = db.relationship('Student', backref='bookings')
    room = db.relationship('Room', backref='bookings')

# 2. Schemas
class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)

class RoomSchema(Schema):
    id = fields.Int(dump_only=True)
    room_number = fields.Str(required=True, validate=validate.Length(min=1))
    capacity = fields.Int(required=True)

class BookingSchema(Schema):
    id = fields.Int(dump_only=True)
    student_id = fields.Int(required=True)
    room_id = fields.Int(required=True)
    check_in_date = fields.Date(required=True)
    check_out_date = fields.Date()
    
    student = fields.Nested(StudentSchema, dump_only=True)
    room = fields.Nested(RoomSchema, dump_only=True)
    
    @post_load
    def validate_booking(self, data, **kwargs):
        room = Room.query.get(data['room_id'])
        if room and len(room.bookings) >= room.capacity:
            raise ValidationError(f'Room {room.room_number} is full.')
        return data

# Instantiate Schemas
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

# 3. Endpoints

# Student Endpoints
@app.route('/students', methods=['POST'])
def create_student():
    data = request.json
    try:
        # Validate and deserialize input data
        student = student_schema.load(data)
        
        # Check if the email already exists
        if Student.query.filter_by(email=student['email']).first():
            return jsonify({"error": "Email already exists."}), 400
        
        # Create a new student instance
        new_student = Student(**student)
        db.session.add(new_student)  # Add to the session
        db.session.commit()          # Commit changes to the database
        return jsonify(student_schema.dump(new_student)), 201  # Return the new student as JSON
    except ValidationError as e:
        return jsonify(e.messages), 400  # Return validation error messages
    except IntegrityError:
        db.session.rollback()  # Rollback the session in case of IntegrityError
        return jsonify({"error": "Email already exists."}), 400  # Return a friendly error message


@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()  # Fetch all students from the database
    return jsonify(students_schema.dump(students)), 200  # Return the list of students

# Room Endpoints
@app.route('/rooms', methods=['POST'])
def create_room():
    data = request.json
    try:
        room = room_schema.load(data)  # Validate and deserialize input data
        new_room = Room(**room)        # Create a new room instance
        db.session.add(new_room)       # Add to the session
        db.session.commit()            # Commit changes to the database
        return jsonify(room_schema.dump(new_room)), 201  # Return the new room as JSON
    except ValidationError as e:
        return jsonify(e.messages), 400  # Return validation error messages

@app.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()  # Fetch all rooms from the database
    return jsonify(rooms_schema.dump(rooms)), 200  # Return the list of rooms

# Booking Endpoints
@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    try:
        booking = booking_schema.load(data)  # Validate and deserialize input data
        new_booking = Booking(**booking)     # Create a new booking instance
        db.session.add(new_booking)          # Add to the session
        db.session.commit()                  # Commit changes to the database
        return jsonify(booking_schema.dump(new_booking)), 201  # Return the new booking as JSON
    except ValidationError as e:
        return jsonify(e.messages), 400  # Return validation error messages

@app.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()  # Fetch all bookings from the database
    return jsonify(bookings_schema.dump(bookings)), 200  # Return the list of bookings

# Main
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all tables
    app.run(debug=True)  
