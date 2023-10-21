from flask import Flask, redirect, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, UserMixin,login_required,logout_user,login_user,LoginManager,current_user, user_accessed, user_logged_in
import mysql.connector
from flask.helpers import url_for
from werkzeug.security import generate_password_hash, check_password_hash


# my database connection
local_server=True
app=Flask(__name__)
app.secret_key='plms'


# for getting unique user access

login_manager=LoginManager(app)
login_manager.login_view='login'

# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://username:password@localhost/database name'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:Suhas@2324@localhost/parking_lot'
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
    phone=db.Column(db.String(20))
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


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        id = request.form.get('cid')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        uname = request.form.get('uname')
        password = request.form.get('password')
        
        # Check if the username or email already exists
        existing_user = Customer.query.filter_by(user_name=uname).first()
        existing_email = Customer.query.filter_by(email=email).first()
        
        if existing_user:
            flash('Username already exists. Please choose another one.', 'error')
        elif existing_email:
            flash('Email address is already registered.', 'error')
        else:
            # Hash the password before storing it
            encpassword = generate_password_hash(password)
            new_user = Customer(
                cust_id=id,
                first_name=fname,
                last_name=lname,
                email=email,
                phone_number=phone,
                address=address,
                user_name=uname,
                password=encpassword
            )
            db.session.add(new_user)
            db.session.commit()
            flash('User added successfully!', 'success')
            return redirect(url_for('signup'))  # Redirect to the signup page

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
