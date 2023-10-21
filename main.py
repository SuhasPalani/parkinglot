from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, UserMixin,login_required,logout_user,login_user,LoginManager,current_user, user_accessed, user_logged_in
import mysql.connector
from flask.helpers import url_for
from werkzeug.security import generate_password_hash, check_password_hash


# my database connection
local_server=True
app=Flask(__name__)
app.secret_key='parking_lot'


# for getting unique user access

login_manager=LoginManager(app)
login_manager.login_view='login'

# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://username:password@localhost/database name'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/parking_lot'
db=SQLAlchemy(app)


@login_manager.user_loader
def load_user(customer_id):
    return user_accessed.query.get(int(customer_id))




class Test(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))

class Customer(db.Model):
    cust_id=db.Column(db.Integer, primary_key=True)
    fname=db.Column(db.String(20))
    lname=db.Column(db.String(20))
    email=db.Column(db.String(50))
    phone=db.Column(db.String(50))
    address=db.Column(db.String(50))
    uname=db.Column(db.String(20))
    password=db.Column(db.String(20))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/usersignup")
def usersignup():
    return render_template("usersignup.html")


@app.route("/userlogin")
def userlogin():
    return render_template("userlogin.html")


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        id=request.POST.get('id')
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        email=request.form.get('email')
        phone=request.form.get('phone')
        address=request.form.get('Address')
        uname=request.form.get('uname')
        password=request.form.get('password')
        # print(fname,lname,email,phone,Address,uname,password)
        encpassword = generate_password_hash(password)
        # emailUser = user_accessed.query.filter_by(email=email).first()
        # if emailUser:
        #     flash('Account for given email already exits, Please Login ', 'warning')
        #     return render_template('login.html')
        # else:
        new_user = db.engine.execute (f"INSERT INTO `customer` (`cust_id `, `first_name`,`last_name`,`email`, `phone_number`, `address`, `user_name`,`password`) VALUES ('{id}', '{fname}','{lname}','{email}', '{phone}', '{address}', '{uname}','{encpassword}' )")
        #user = User.query.filter_by(email=email).first()
        # flash('User account created', 'success')
        # return render_template('index.html')
        return 'úser added'
    return render_template("usersignup.html")




















# testing db connection
@app.route("/test")
def test():
    try:
        a=Test.query.all()
        print(a)
        # return 'DB connected'
        return f'{a.name}'
    
    except Exception as e:
        print(e)
        return 'db not connected'



app.run(debug=True)
