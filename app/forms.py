from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField, PasswordField
from wtforms.validators import InputRequired, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class BookingForm(FlaskForm):
    hotel_name = StringField('Hotel Destination', validators=[InputRequired()])
    room = StringField('Room Name', validators=[InputRequired()])
    check_in_date = DateField('Check In Date', validators=[InputRequired()], format='%d/%m/%Y')
    check_out_date = DateField('Check Out Date', validators=[InputRequired()], format='%d/%m/%Y')
    num_guests = IntegerField('Number of Guests', validators=[InputRequired()])
    cust_fname = StringField('First Name', validators = [InputRequired()])
    cust_lname = StringField('Last Name', validators = [InputRequired()])
    cust_age = IntegerField('Age', validators=[InputRequired()])
    cust_email = StringField('Email Address', validators=[InputRequired()])
    cust_phone_number = StringField('Phone Number', validators=[InputRequired()])
    submit = SubmitField('Send', validators = [InputRequired()])

class DeleteBooking(FlaskForm):
    deleteID = IntegerField('Booking ID', validators=[InputRequired()])
    delete = SubmitField('Delete')

class HotelForm(FlaskForm):
    hotel_name = StringField('Hotel Destination', validators=[InputRequired()])
    rooms = StringField('Room Name', validators=[InputRequired()])
    price = IntegerField('Hotel Price', validators=[InputRequired()])
    rating = IntegerField('Rating Out of 5', validators=[InputRequired(), NumberRange(min=1, max=5)])
    availability = StringField('Availability', validators=[InputRequired()])
    submit = SubmitField('Send', validators = [InputRequired()])

class DelHotel(FlaskForm):
    deleteID = IntegerField('Hotel ID',validators=[InputRequired()])
    delete = SubmitField('Delete')

class SearchForm(FlaskForm):
    query = StringField('Search')
    submit = SubmitField('Send',validators=[InputRequired()])