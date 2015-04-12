# FlaskAuth
A web app written with Python Flask framework that allows users to create accounts, login, and modify there information. Code is commented and provides tutorials for flask, sql and jinja2 templating. Might provide app specific documentation later. 

**NOTE**
This app is a stripped down, ugly example from a larger app I am building. I am posting it here as a resource for others to use to learn Flask and start playing with the framework in a development environment.


To start using this code quickly follow these steps.

1.) create a free account at pythonanywhere.com
2.) in the consoles tab open a bash console and run the following;
    git init
    git clone https://github.com/socialpanic/FlaskAuth.git
3.) this should Clone this entire repo and create a FlaskAuth folder in your pythonanywhere directory.
4.) in the Web tab create a new web app. Select flask framework, and Python 2.7.
5.) When the Path appears on the next screen remove "mysite" from the path and add "FlaskAuth". Leave everything else in the path alone!!
6.) Now go to the files tab. Open FlaskAuth and look for the run.py file. Copy its single line of code to file that the web app wizard created in step 5.
7.) To set up the database go to the Database tab and set a SQL password. Then create a database. Before leaving this screen note the following; server name, mysql username, mysql password (you just set it), and finally the database name(you just named it)
8.) Take the information from the database you created in step 7 and go to FlaskAuth/app/views.py and at about line 20 where the mysql database connection credientials are, populate the code with YOUR server name, username, password, and name of database
9.) Next go to the Upload Folder variable at around line 30 and change it to make sure it reflects the path to YOUR profilepics folder in static/images.
10.) Finally, go to db.txt in the root of the repo and copy the sql code at the bottom. Go to the consoles tab again and open a MySQL console.
11.) In the MySQL console run 'show databases;' and look for the one you created in step 7. Once you see it type 'use that$database' where that$database is the database YOU created in STEP 7 and not this instructional place holder.
12.) Now paste the Create Table code from Step 10 into the console (control+v).

That is all folks. now go to the Web tab and click on the big url for your app. if everything went well you should be greeted with the apps index page and the join / signin boxes. If ANY part of this was screwed up dont expect it to work since the app depends on the database being configured as outlined.

I will try to release a screen cast about this if there are very many problems.
