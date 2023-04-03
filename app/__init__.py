from flask import Flask
import psycopg2
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate =   Migrate(app,db)


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
        cust_lname VARCHAR(255) NOT NULL
    );
""")

#Hotel list init

cur.execute("""
    CREATE TABLE IF NOT EXISTS hotels_list (
        hotelid SERIAL PRIMARY KEY,
        hotel_name VARCHAR(255) NOT NULL,
        rooms varchar(255) NOT NULL
    );
""")

conn.commit()

cur.close()
conn.close()



