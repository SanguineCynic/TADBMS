from flask import Flask
from flask_login import LoginManager
import psycopg2
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate =   Migrate(app,db)


# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views

conn = psycopg2.connect(
    host="localhost",
    database="Bookings",
    user="postgres",
    password="Redfire3"
)

cur = conn.cursor()

#Bookings init

cur.execute("""
    CREATE TABLE IF NOT EXISTS hotel_bookings (
        bookingid SERIAL PRIMARY KEY,
        hotel_name VARCHAR(255) NOT NULL,
        check_in_date DATE NOT NULL,
        check_out_date DATE NOT NULL,
        num_guests INTEGER NOT NULL,
        cust_fname VARCHAR(255) NOT NULL,
        cust_lname VARCHAR(255) NOT NULL,
        cust_age INTEGER NOT NULL,
        cust_email VARCHAR(255) NOT NULL,
        cust_phone_number VARCHAR(20),
        confirmed BOOLEAN NOT NULL
    );
""")

#Hotel list init

cur.execute("""
    CREATE TABLE IF NOT EXISTS hotels_list (
        hotelid SERIAL PRIMARY KEY,
        hotel_name VARCHAR(255) NOT NULL,
        rooms VARCHAR(255) NOT NULL,
        price INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        availability VARCHAR(255) NOT NULL
    );
""")

#Archives init

cur.execute("""
    CREATE TABLE IF NOT EXISTS archives (
        bookingid INTEGER NOT NULL,
        hotel_name VARCHAR(255) NOT NULL,
        check_in_date DATE NOT NULL,
        check_out_date DATE NOT NULL,
        num_guests INTEGER NOT NULL,
        cust_fname VARCHAR(255) NOT NULL,
        cust_lname VARCHAR(255) NOT NULL,
        cust_age INTEGER NOT NULL,
        cust_email VARCHAR(255) NOT NULL,
        cust_phone_number VARCHAR(20)
    );
""")

conn.commit()

cur.close()
conn.close()



