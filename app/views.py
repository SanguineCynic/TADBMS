import os, psycopg2
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from app.models import HotelBooking, Hotel, UserProfile, Archive
from .forms import BookingForm, DeleteBooking, HotelForm, DelHotel, SearchForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

@app.route('/', methods=['GET','POST'])
@login_required
def home():
    searchFormObj = SearchForm()
    hotels = Hotel.query.all()
    bookings = HotelBooking.query.all()

    if 'sort' in request.args:
        sort_column = request.args['sort']
        if sort_column == 'bookingid':
            bookings = sorted(bookings, key=lambda x: x.bookingid)
        elif sort_column == 'firstname':
            bookings = sorted(bookings, key=lambda x: x.cust_fname)
        elif sort_column == 'lastname':
            bookings = sorted(bookings, key=lambda x: x.cust_lname)
        elif sort_column == 'hotelname':
            bookings = sorted(bookings, key=lambda x: x.hotel_name)
        elif sort_column == 'hotelid':
            hotels = sorted(hotels, key=lambda x: x.hotelid)
        elif sort_column == 'room':
            hotels = sorted(hotels, key=lambda x: x.rooms)
        elif sort_column == 'hotel_name':
            hotels = sorted(hotels, key=lambda x: x.hotel_name)

    if searchFormObj.is_submitted():
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
            return render_template('home.html', bookings = bookings, hotels= hotels, form = searchFormObj)
        
        print(bookingrows)

        conn.commit()

        cur.close()
        conn.close()

        return render_template('search.html', bookingrows = bookingrows, hotelrows= hotelrows, form = searchFormObj)
    
    return render_template('home.html', bookings = bookings, hotels= hotels, form = searchFormObj)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Get the username and password values from the form.
        res = request.form
        formUsername = res['username']
        formPassword = res['password']

        user =  UserProfile.query.filter_by(username = formUsername)
        # user = userQuery[0]
        if check_password_hash(user[0].password, formPassword):
            # Gets user id, load into session
            login_user(user[0])
            flash("Successful login")
            return redirect(url_for("home"))

    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You are now logged out")
    return redirect(url_for('login'))

@app.route('/addbooking', methods=['GET','POST'])
@login_required
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
            'cust_lname': res['cust_lname'],
            'cust_age' : res['cust_age'], 
            'cust_email' : res['cust_email'],
            'cust_phone_number' : res['cust_phone_number']
        }

        checkHotel = Hotel.query.filter_by(hotel_name=res['hotel_name']).first()
        checkRoom = Hotel.query.filter_by(hotel_name=res['hotel_name'], rooms=res['room']).first()

        if checkHotel is not None and checkRoom is not None:
            cur.execute("""
                INSERT INTO hotel_bookings (hotel_name, check_in_date, check_out_date, num_guests, cust_fname, cust_lname, cust_age, cust_email, cust_phone_number, confirmed)
                VALUES (%(hotel_name)s, %(check_in_date)s, %(check_out_date)s, %(num_guests)s, %(cust_fname)s, %(cust_lname)s, %(cust_age)s, %(cust_email)s, %(cust_phone_number)s, FALSE);
            """, booking_data)

            conn.commit()
    
            cur.close()
            conn.close()
        else:

            conn.commit()

            cur.close()
            conn.close()

            if checkHotel is None:
                flash("Invalid hotel name")
            elif checkRoom is None:
                flash("Invalid room name")

            return render_template('storebooking.html', form=formObj)


        return redirect(url_for('home'))

    return render_template('storebooking.html', form=formObj)

@app.route('/bookings', methods=['GET','POST'])
@login_required
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

        check = HotelBooking.query.filter_by(bookingid=res['changeID']).first()

        if check is not None:
            booking_data = {
            'hotel_name': res['hotel_name'],
            'check_in_date': res['check_in_date'],
            'check_out_date': res['check_out_date'],
            'num_guests': res['num_guests'],
            'cust_fname': res['cust_fname'],
            'cust_lname': res['cust_lname'],
            'cust_age' : res['cust_age'], 
            'cust_email' : res['cust_email'],
            'cust_phone_number' : res['cust_phone_number'],
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
                cust_lname = %(cust_lname)s,
                cust_age = %(cust_age)s,
                cust_email = %(cust_email)s,
                cust_phone_number = %(cust_phone_number)s,
                confirmed = FALSE
                WHERE bookingid = %(changeID)s;
            """, booking_data)

        else:
            flash("Booking ID does not exist")

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('update'))

    return render_template('updatebookings.html', data=resMain, form=BookingformObj)

@app.route('/deletebooking', methods=['GET','POST'])
@login_required
def delete():
    resMain = HotelBooking.query.all()
    DelformObj = DeleteBooking()
    # print("#EASY MONEY#")

    if DelformObj.is_submitted():
        res = request.form

        conn = psycopg2.connect(
            host="localhost",
            database="Bookings",
            user="postgres",
            password="Redfire3"
        )
        cur = conn.cursor()

        check = HotelBooking.query.filter_by(bookingid=res['deleteID']).first()

        if check is not None:
            cur.execute("""DELETE FROM hotel_bookings WHERE bookingid = %(deleteID)s""", res)
        else:
            flash("Booking ID not found")
        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('update'))

    return render_template('deleteform.html', data=resMain, delform=DelformObj)

@app.route('/conf/<int:bookingid>', methods=['GET','POST'])
@login_required
def confirm(bookingid):
    check = HotelBooking.query.filter_by(bookingid=bookingid, confirmed=False).first()

    conn = psycopg2.connect(
            host="localhost",
            database="Bookings",
            user="postgres",
            password="Redfire3"
        )
    cur = conn.cursor()

    if check is not None:
        cur.execute("""UPDATE hotel_bookings SET confirmed = TRUE WHERE bookingid = %s""", (bookingid,))
    else:
        cur.execute("""UPDATE hotel_bookings SET confirmed = FALSE WHERE bookingid = %s""", (bookingid,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('home'))

@app.route('/addhotel', methods=['GET','POST'])
@login_required
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
            'rooms' : res['rooms'],
            'price' : res['price'],
            'rating' : res['rating'],
            'availability' : res['availability']
        }

        cur.execute("""
            INSERT INTO hotels_list (hotel_name, rooms, price, rating, availability)
            VALUES (%(hotel_name)s, %(rooms)s,%(price)s,%(rating)s,%(availability)s);
        """, hotel_data)

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('addhotel.html', form=formObj, data=resMain)

@app.route('/hotels', methods=['GET','POST'])
@login_required
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

        check = Hotel.query.filter_by(hotelid=res['changeID']).first()

        if check is not None:
            hotel_data = {
                'hotel_name': res['hotel_name'],
                'rooms' : res['rooms'],
                'price' : res['price'],
                'rating' : res['rating'],
                'availability' : res['availability'],
                'changeID' : res['changeID']
            }

            cur.execute("""
                UPDATE hotels_list
                SET
                hotel_name = %(hotel_name)s,
                rooms = %(rooms)s,
                price = %(price)s,
                rating = %(rating)s,
                availability = %(availability)s
                WHERE hotelid = %(changeID)s;
            """, hotel_data)
        else:
            flash("Hotel ID does not exist")

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('updatehotel'))

    return render_template('updatehotel.html', hotels=resMain, form=formObj)

@app.route('/deletehotel', methods = ['GET','POST'])
@login_required
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

        check = Hotel.query.filter_by(hotelid=res['deleteID']).first()

        if check is not None:
            cur.execute("""DELETE FROM hotels_list WHERE hotelid = %(deleteID)s""", res)
        else:
            flash("Hotel ID does not exist")
            cur.close()
            conn.close()

            return render_template('deletehotel.html', hotels=resMain, delform=DelformObj)
        
        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('deletehotel.html', hotels=resMain, delform=DelformObj)

@app.route('/archive', methods = ['GET','POST'])
@login_required
def archivebooking():
    bookingsToArchive = HotelBooking.query.filter(HotelBooking.check_out_date < date.today()).all()

    conn = psycopg2.connect(
    host="localhost",
    database="Bookings",
    user="postgres",
    password="Redfire3"
    )
    cur = conn.cursor()

    if bookingsToArchive:
        for entry in bookingsToArchive:
            # Insert the booking into the archives table
            cur.execute(
                "INSERT INTO archives (bookingid, hotel_name, check_in_date, check_out_date, num_guests, cust_fname, cust_lname, cust_age, cust_email, cust_phone_number ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (entry.bookingid, entry.hotel_name, entry.check_in_date, entry.check_out_date, entry.num_guests, entry.cust_fname, entry.cust_lname, entry.cust_age, entry.cust_email, entry.cust_phone_number )
            )
    
            # Delete the booking from the hotel_bookings table
    
            cur.execute(
                "DELETE FROM hotel_bookings WHERE bookingid = %s",
                (entry.bookingid,)
            )

    conn.commit()

    cur.close()
    conn.close()

    archBookings = Archive.query.all()

    if 'sort' in request.args:
        sort_column = request.args['sort']
        if sort_column == 'bookingid':
            archBookings = sorted(archBookings, key=lambda x: x.bookingid)
        elif sort_column == 'firstname':
            archBookings = sorted(archBookings, key=lambda x: x.cust_fname)
        elif sort_column == 'lastname':
            archBookings = sorted(archBookings, key=lambda x: x.cust_lname)
        elif sort_column == 'hotelname':
            archBookings = sorted(archBookings, key=lambda x: x.hotel_name)

    return render_template('archive.html', bookings = archBookings)

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')