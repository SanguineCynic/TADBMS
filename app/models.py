from . import db
from flask import Flask, request
from werkzeug.security import generate_password_hash

app = Flask(__name__)

class HotelBooking(db.Model):

    __tablename__ = "hotel_bookings"

    bookingid = db.Column(db.Integer, primary_key=True)
    hotel_name = db.Column(db.String(60))
    check_in_date = db.Column(db.DATE)
    check_out_date = db.Column(db.DATE)
    num_guests = db.Column(db.Integer)
    cust_fname = db.Column(db.String(60))
    cust_lname = db.Column(db.String(60))
    cust_age = db.Column(db.Integer)
    cust_email = db.Column(db.String(60))
    cust_phone_number = db.Column(db.String(15))
    confirmed = db.Column(db.Boolean)

    def __init__(self, booking_id, hotel_name, check_in_date, check_out_date, num_guests, cust_fname, cust_lname, cust_age, cust_email, cust_phone_number):
        self.booking_id = booking_id
        self.hotel_name = hotel_name
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.num_guests = num_guests
        self.cust_fname = cust_fname
        self.cust_lname = cust_lname
        self.cust_age = cust_age 
        self.cust_email = cust_email
        self.cust_phone_number = cust_phone_number
        self.confirmed = False

class Hotel(db.Model):

    __tablename__ = "hotels_list"

    hotelid = db.Column(db.Integer, primary_key=True)
    hotel_name = db.Column(db.String(60))
    rooms = db.Column(db.String(200))
    price = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    availability = db.Column(db.String(100))

    def __init__(self, hotel_id, hotel_name, rooms, price, rating, availability):
        self.hotel_id = hotel_id
        self.hotel_name = hotel_name
        self.rooms = rooms
        self.price = price
        self.rating = rating
        self.availability = availability

class Archive(db.Model):

    __tablename__ = "archives"

    bookingid = db.Column(db.Integer, primary_key=True)
    hotel_name = db.Column(db.String(60))
    check_in_date = db.Column(db.DATE)
    check_out_date = db.Column(db.DATE)
    num_guests = db.Column(db.Integer)
    cust_fname = db.Column(db.String(60))
    cust_lname = db.Column(db.String(60))
    cust_age = db.Column(db.Integer)
    cust_email = db.Column(db.String(60))
    cust_phone_number = db.Column(db.String(15))

    def __init__(self, booking_id, hotel_name, check_in_date, check_out_date, num_guests, cust_fname, cust_lname, cust_age, cust_email, cust_phone_number):
        self.booking_id = booking_id
        self.hotel_name = hotel_name
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.num_guests = num_guests
        self.cust_fname = cust_fname
        self.cust_lname = cust_lname
        self.cust_age = cust_age 
        self.cust_email = cust_email
        self.cust_phone_number = cust_phone_number

class UserProfile(db.Model):
  
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
