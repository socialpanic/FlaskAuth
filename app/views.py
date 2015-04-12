
from flask import render_template, session, request, redirect, url_for, jsonify
from collections import Counter
from app import app
import MySQLdb
import os, datetime
import time
import datetime
import random
import itertools
import json

#Note: This is actually a stripped down product from a larger app
#I built and not all of the above imports are necessary to run this
#app but I am lazy and left them.

msg=''
data = {}
'''
be sure to edit this information with the creditentials for YOUR sql server
'''
def dbconnect():
    mysql2 = MySQLdb.connect(host= "mysql.server",
        user="wvup",
        passwd="pass",
        db="wvup$hawkcrypt")
    return mysql2

'''

Did you change the mysql connect information to match YOUR mysql server????
'''
def read_students():

    db = dbconnect()
    conn = db.cursor()
    conn.execute("SELECT * FROM Students")
    data = conn.fetchall()
    data=list(data)
    return data



'''
CHANGE UPLOAD_FOLDER PATH
'''
UPLOAD_FOLDER = "/home/wvup/mysite/projecttreequo/app/static/imgs/profilepics/"
'''
DID YOU CHANGE THE UPLOAD_FOLDER PATH?
'''
key_seed = str(datetime.datetime.now())
app.config['SECRET_KEY'] = 'abcdefghijklmnopqrstuvwxyz'+key_seed+str(random.randint(0, 5000));
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods = ['GET', 'POST'])
def index():
        return render_template('index.html')

@app.route('/home',  methods = ['GET', 'POST'])
def home():
        logged=True
        data.clear()
        studentdata = read_students()
        data["students"] = studentdata

        if os.path.isfile(UPLOAD_FOLDER+session['username']+"pic") == True:
            profilepic = str(session['username']+"pic")
            return render_template ("member.html", logged=logged, profilepic=profilepic, session=session, data=data)
        else:
            return render_template ("member.html", logged=logged, session=session, data=data)

@app.route("/login", methods = ['GET', 'POST'])
def login():
	msg = ""
	db = dbconnect()
	conn = db.cursor()
	session["username"] = request.form["user"]
	session["password"] = request.form["pass"]
	conn.execute("SELECT * from Users where username='" + session["username"] + "' and password='" + session["password"] + "'")
	userdata = conn.fetchone()
	if userdata is None:
		logged = False
		msg = "Username or Password is wrong"
		return render_template ('index.html', msg=msg, logged=logged)
	else:
		logged = True
		session["logged_in"] = True
		session["userdata"] = userdata
		if os.path.isfile(UPLOAD_FOLDER+session['username']+"pic") == True:
		    profilepic = str(session['username']+"pic")
		    return redirect(url_for('home'))
		else:
		    return redirect(url_for('home'))
		conn.close()
	return render_template ('index2.html', msg=msg, logged=logged)

@app.route('/logout')
def logout():
	msg = "You are now signed out"
	session.pop('logged_in', None)
	logged = False
	return render_template('index.html', msg=msg, logged=logged)


@app.route('/editprofile', methods = ['GET', 'POST'])
def editprofile():
        logged = True
        if os.path.isfile(UPLOAD_FOLDER+session['username']+"pic") == True:
            profilepic = str(session['username']+"pic")
            return render_template("editprofile.html", session=session, profilepic=profilepic, username=session['username'])
        else:
		    return render_template("editprofile.html", session=session, username=session['username'])

@app.route("/join", methods = ['GET', 'POST'])
def join():
    db = dbconnect()
    conn = db.cursor()
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    username = request.form["username"]
    password = request.form["password"]
    confirmpass = request.form["confirmpass"]
    email = request.form["email"]

    if password == confirmpass:
		conn.execute("SELECT * FROM Users WHERE username='" + username + "' OR email='" + email + "'")
		data = conn.fetchone()
		if data is None:
		    msg = "Creating Account. Please try logging in."
		    path = os.curdir
		    conn.execute("INSERT INTO Users (UID, firstname, lastname, email, password, username) VALUES ('DEFAULT', '"+firstname+"', '"+lastname+"', '"+email+"', '"+password+"', '"+username+"')")
		    logged = False
		    MySQLdb.connection.commit(db)
		    return render_template ('index.html', msg=msg, logged=logged)
		else:
		    logged = False
		    msg = "An account with that username or email already exists"
		    return render_template ('index.html', msg=msg, logged=logged)
    else:
        msg = "The passwords do not match. Please try again."
        return render_template ('index.html', msg=msg)

@app.route('/update_profile', methods=['GET','POST'])
def update_profile():
    if session["logged_in"] == True:
        username = session['username']

        conn = dbconnect()
        setstring = ""

        firstname = request.form["firstname"]
        if firstname != "":
    	    setstring = setstring + "firstname ='" + firstname +"'"
        lastname = request.form["lastname"]
        if lastname != "" and setstring != "":
            setstring = setstring + ", lastname ='" + lastname +"'"
        elif lastname != "" and setstring == "":
           setstring = setstring + "lastname ='" + lastname +"'"
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password == confirm_password:
            if password != "" and setstring != "":
                setstring = setstring + ", password ='" + password +"'"
            elif password != "" and setstring == "":
               setstring = setstring + "password ='" + password +"'"

        querystring = "UPDATE Users SET "+setstring+" WHERE username = '"+str(username)+"';"
        testdata = conn.execute(querystring)

        MySQLdb.connection.commit(mysql2)
        conn.execute("SELECT * FROM Users WHERE username = '"+str(username)+"'")
        data = conn.fetchone()
        session["userdata"]=data
        MySQLdb.connection.commit(mysql2)


        if os.path.isfile(UPLOAD_FOLDER+session['username']+"pic") == True:
            logged = True
    	    profilepic = str(session['username']+"pic")
    	    return redirect(url_for('home'))

    	else:
    	    logged = True
    	    return redirect(url_for('home'))

    else:
        return "testing testing 2 not logged"


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if session["logged_in"] == True:
    	if request.method == 'POST':
    		file = request.files['file']

	        conn = dbconnect()
	        conn.execute("SELECT * FROM Users WHERE username = '"+str(session['username'])+"'")
	        MySQLdb.connection.commit(mysql2)
	        data = conn.fetchone()


    		if file and allowed_file(file.filename):
    		    logged = True
    		    filename = session['username']+'pic'
    		    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    		    profilepic = str(session['username']+"pic")
    		    conn.execute("UPDATE Users SET profilepic = '"+profilepic+"' WHERE username = '"+str(session['username'])+"'")
    		    MySQLdb.connection.commit(mysql2)
    		    return redirect(url_for('home'))

@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
    db = dbconnect()
    conn = db.cursor()

    fname = request.form["new_student_fname"]
    lname = request.form["new_student_lname"]
    age = request.form["new_student_age"]
    birthmonth = request.form["new_student_dob_month"]
    birthday = request.form["new_student_dob_day"]
    birthyear = request.form["new_student_birthyear"]
    phone = request.form["new_student_phone"]
    email = request.form["new_student_email"]
    address1 = request.form["new_student_address1"]
    address2 = request.form["new_student_address2"]
    city = request.form["new_student_city"]
    state = request.form["new_student_state"]
    zipcode = request.form["new_student_zip"]
    major = request.form["new_student_major"]
    advisor = request.form["new_student_advisor"]
    gpa = request.form["new_student_gpa"]
    password = request.form["new_student_password"]
    confirmpass = request.form["confirmpass"]
    credithours = request.form["new_student_credits"]
    licenseplate = request.form["new_student_license"]



    if password == confirmpass:
		conn.execute("SELECT * FROM Students WHERE email='"+email+"'")
		data = conn.fetchone()
		if data is None:
		    logged = True
		    msg = "Student Added to Database"
		    conn.execute("INSERT INTO Students (sid, fname, lname, age, birth_month, birth_day, birth_year, phone, email, address1, address2, city, state, zip, major, advisor, gpa, password, credit_hours, license_plate) VALUES ('DEFAULT', '"+fname+"', '"+lname+"', '"+age+"', '"+birthmonth+"', '"+birthday+"', '"+birthyear+"', '"+phone+"','"+email+"','"+address1+"','"+address2+"','"+city+"','"+state+"','"+zipcode+"','"+major+"','"+advisor+"','"+gpa+"','"+password+"','"+credithours+"','"+licenseplate+"')")
		    MySQLdb.connection.commit(db)
		    return redirect(url_for('home'))
		else:
		    logged = False
		    msg = "A student with that email address already exists"
		    return redirect(url_for('home'))
    else:
      msg = "Logged Out. Please Try Again"
      return render_template ('index.html', msg=msg)

@app.route('/delete_student', methods=['GET', 'POST'])
def delete_student(x):
    return x

@app.route('/delete/<x>', methods = ['GET', 'POST'])
def answer(x):
    db = dbconnect()
    conn = db.cursor()
    query = "DELETE FROM Students WHERE sid = "+x+";"

    conn.execute(query)
    MySQLdb.connection.commit(db)
    return redirect(url_for('home'))




