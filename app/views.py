import os, psycopg2
from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models import HotelBooking, Hotel
from .forms import BookingForm, DeleteBooking, HotelForm, DelHotel, SearchForm

@app.route('/', methods=['GET','POST'])
def home():
    formObj = SearchForm()
    hotels = Hotel.query.all()
    bookings = HotelBooking.query.all()

    if formObj.is_submitted():
        res = request.form
        # print(res['changeID'])

        conn = psycopg2.connect(
            host="localhost",
            database="Bookings",
            user="postgres",
            password="Redfire3"
        )
        cur = conn.cursor()
        
        cur.execute("""SELECT * FROM hotel_bookings 
        WHERE hotel_name=%s OR cust_fname=%s OR cust_lname=%s""", 
        (res['query'], res['query'], res['query']))
        bookingrows = cur.fetchall()

        cur.execute("""SELECT * FROM hotels_list
        WHERE hotel_name=%s OR rooms=%s""",
        (res['query'],res['query']))
        hotelrows = cur.fetchall()

        if bookingrows == [] and hotelrows == []:
            return render_template('home.html', bookings = bookings, hotels= hotels, form = formObj)
        
        print(bookingrows)

        # conn.commit()

        cur.close()
        conn.close()

        return render_template('search.html', bookingrows = bookingrows, hotelrows= hotelrows, form = formObj)

    
    return render_template('home.html', bookings = bookings, hotels= hotels, form = formObj)

@app.route('/addbooking', methods=['GET','POST'])
def bookings():

    formObj = BookingForm()
    if formObj.is_submitted():
        res = request.form
        conn = psycopg2.connect(
            host="localhost",
            database="Bookings",
            user="postgres",
            password="Redfire3"
        )
        cur = conn.cursor()

        booking_data = {
            'hotel_name': res['hotel_name'],
            'check_in_date': res['check_in_date'],
            'check_out_date': res['check_out_date'],
            'num_guests': res['num_guests'],
            'cust_fname': res['cust_fname'],
            'cust_lname': res['cust_lname']
        }

        cur.execute("""
            INSERT INTO hotel_bookings (hotel_name, check_in_date, check_out_date, num_guests, cust_fname, cust_lname)
            VALUES (%(hotel_name)s, %(check_in_date)s, %(check_out_date)s, %(num_guests)s, %(cust_fname)s, %(cust_lname)s);
        """, booking_data)

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('storebooking.html', form=formObj)

@app.route('/bookings', methods=['GET','POST'])
def update():
    resMain = HotelBooking.query.all()
    # print(resMain)
    BookingformObj = BookingForm()

    if BookingformObj.is_submitted():
        res = request.form
        # print(res['changeID'])

        conn = psycopg2.connect(
            host="localhost",
            database="Bookings",
            user="postgres",
            password="Redfire3"
        )
        cur = conn.cursor()

        booking_data = {
            'hotel_name': res['hotel_name'],
            'check_in_date': res['check_in_date'],
            'check_out_date': res['check_out_date'],
            'num_guests': res['num_guests'],
            'cust_fname': res['cust_fname'],
            'cust_lname': res['cust_lname'],
            'changeID' : res['changeID']
        }

        cur.execute("""
            UPDATE hotel_bookings
            SET
            hotel_name = %(hotel_name)s,
            check_in_date = %(check_in_date)s,
            check_out_date = %(check_out_date)s,
            num_guests = %(num_guests)s,
            cust_fname = %(cust_fname)s,
            cust_lname = %(cust_lname)s
            WHERE bookingid = %(changeID)s;
        """, booking_data)

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('update'))

    return render_template('updatebookings.html', data=resMain, form=BookingformObj)

@app.route('/deletebooking', methods=['GET','POST'])
def delete():
    resMain = HotelBooking.query.all()
    DelformObj = DeleteBooking()
    print("#EASY MONEY#")

    if DelformObj.is_submitted():
        res = request.form

        conn = psycopg2.connect(
            host="localhost",
            database="Bookings",
            user="postgres",
            password="Redfire3"
        )
        cur = conn.cursor()

        cur.execute("""DELETE FROM hotel_bookings WHERE bookingid = %(deleteID)s""", res)

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('update'))

    return render_template('deleteform.html', data=resMain, delform=DelformObj)

@app.route('/addhotel', methods=['GET','POST'])
def hotels():
    resMain = Hotel.query.all()
    print(resMain)
    formObj = HotelForm()
    if formObj.is_submitted():
        res = request.form
        conn = psycopg2.connect(
            host="localhost",
            database="Bookings",
            user="postgres",
            password="Redfire3"
        )
        cur = conn.cursor()

        hotel_data = {
            'hotel_name': res['hotel_name'],
            'rooms' : res['rooms']
        }

        cur.execute("""
            INSERT INTO hotels_list (hotel_name, rooms)
            VALUES (%(hotel_name)s, %(rooms)s);
        """, hotel_data)

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('addhotel.html', form=formObj, data=resMain)

@app.route('/hotels', methods=['GET','POST'])
def updatehotel():
    resMain = Hotel.query.all()
    # print(resMain)
    formObj = HotelForm()

    if formObj.is_submitted():
        res = request.form
        # print(res['changeID'])

        conn = psycopg2.connect(
            host="localhost",
            database="Bookings",
            user="postgres",
            password="Redfire3"
        )
        cur = conn.cursor()

        hotel_data = {
            'hotel_name': res['hotel_name'],
            'rooms' : res['rooms'],
            'changeID' : res['changeID']
        }

        cur.execute("""
            UPDATE hotels_list
            SET
            hotel_name = %(hotel_name)s,
            rooms = %(rooms)s
            WHERE hotelid = %(changeID)s;
        """, hotel_data)

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('updatehotel'))

    return render_template('updatehotel.html', hotels=resMain, form=formObj)

@app.route('/deletehotel', methods = ['GET','POST'])
def deletehotel():
    resMain = Hotel.query.all()
    DelformObj = DelHotel()
    print("#EASY MONEY#")

    if DelformObj.is_submitted():
        res = request.form

        conn = psycopg2.connect(
            host="localhost",
            database="Bookings",
            user="postgres",
            password="Redfire3"
        )
        cur = conn.cursor()

        cur.execute("""DELETE FROM hotels_list WHERE hotelid = %(deleteID)s""", res)

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('deletehotel.html', hotels=resMain, delform=DelformObj)

# @app.route('/search')
# def search():
