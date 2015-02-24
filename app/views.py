
from flask import render_template, session, request, redirect, url_for, jsonify
from collections import Counter
from app import app
import MySQLdb
import os, datetime
import time
import datetime
import random
import itertools

#Note: This is actually a stripped down product from a larger app
#I built and not all of the above imports are necessary to run this
#app but I am lazy and left them.

data = []
'''
be sure to edit this information with the creditentials for YOUR sql server
'''
mysql2 = MySQLdb.connect(host= "mysql.server",
    user="wvup",
    passwd="pass",
    db="wvup$hawkcrypt")
'''
Did you change the mysql connect information to match YOUR mysql server????
'''

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
        if os.path.isfile(UPLOAD_FOLDER+session['username']+"pic") == True:
            profilepic = str(session['username']+"pic")
            return render_template ("member.html", logged=logged, profilepic=profilepic, session=session)
        else:
            return render_template ("member.html", logged=logged, session=session)

@app.route("/login", methods = ['GET', 'POST'])
def login():
	msg = ""
	conn = mysql2.cursor()
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

    conn = mysql2.cursor()
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
			path = os.curdir
			conn.execute("INSERT INTO Users (UID, firstname, lastname, email, password, username) VALUES ('DEFAULT', '"+firstname+"', '"+lastname+"', '"+email+"', '"+password+"', '"+username+"')")
			logged = False
			MySQLdb.connection.commit(mysql2)
			return render_template ('index.html', msg=msg, logged=logged)
		else:
		    logged = False
		    msg = "That username or password already exists"
		    return render_template ('index.html', msg=msg, logged=logged)
    else:
        msg = "The passwords do not match. Please try again."
        return render_template ('index.html', msg=msg, logged=logged)

@app.route('/update_profile', methods=['GET','POST'])
def update_profile():
    if session["logged_in"] == True:
        username = session['username']

        conn = mysql2.cursor()
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

	        conn = mysql2.cursor()
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