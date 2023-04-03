from . import db
from flask import Flask, request

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

    def __init__(self, booking_id, hotel_name, check_in_date, check_out_date, num_guests, cust_fname, cust_lname):
        self.booking_id = booking_id
        self.hotel_name = hotel_name
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.num_guests = num_guests
        self.cust_fname = cust_fname
        self.cust_lname = cust_lname

class Hotel(db.Model):

    __tablename__ = "hotels_list"

    hotelid = db.Column(db.Integer, primary_key=True)
    hotel_name = db.Column(db.String(60))
    rooms = db.Column(db.String(200))

    def __init__(self, hotel_id, hotel_name, rooms):
        self.hotel_id = hotel_id
        self.hotel_name = hotel_name
        self.rooms = rooms
        
