How to run the web application:

1) Change postgres password to that of local postgres user credential:
	Line 20 of __init__.py
	Line 6 of .env
	Lines 21, 61, 109 of views.py

2) Add secret key to .env line 4

3) Install requirements:
	pip install -r requirements.txt

4) Create database:
	Open psql
	create user "INSERTUSERNAMEHERE";
	create database "Bookings";
	\password "PREVIOUSUSERNAMEINQUOTES"
	INSERTPASSWORDHERE
	alter database "Bookings" owner to "PREVIOUSNAMEINQUOTES"
	\c "Bookings"
	\dt to ensure all is well



5) Migrate:
	In TADBMS directory, flask db init (likely will not do anything)
	flask db migrate (likely will not do anything)
	flask db upgrade  (may do something)
