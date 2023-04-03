from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField
from wtforms.validators import InputRequired

class BookingForm(FlaskForm):
    hotel_name = StringField('Hotel Name', validators=[InputRequired()])
    check_in_date = DateField('Check In Date', validators=[InputRequired()], format='%d/%m/%Y')
    check_out_date = DateField('Check Out Date', validators=[InputRequired()], format='%d/%m/%Y')
    num_guests = IntegerField('Number of Guests', validators=[InputRequired()])
    cust_fname = StringField('First Name', validators = [InputRequired()])
    cust_lname = StringField('Last Name', validators = [InputRequired()])
    submit = SubmitField('Send', validators = [InputRequired()])

class DeleteBooking(FlaskForm):
    deleteID = IntegerField('Booking ID', validators=[InputRequired()])
    delete = SubmitField('Delete')

class HotelForm(FlaskForm):
    hotel_name = StringField('Hotel Name', validators=[InputRequired()])
    rooms = StringField('Room Name', validators=[InputRequired()])
    submit = SubmitField('Send', validators = [InputRequired()])

class DelHotel(FlaskForm):
    deleteID = IntegerField('Hotel ID',validators=[InputRequired()])
    delete = SubmitField('Delete')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[InputRequired()])
    submit = SubmitField('Send',validators=[InputRequired()])