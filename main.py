from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
# my database connection
local_server=True
app=Flask(__name__)
app.secret_key='parking_lot'

# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://username:password@localhost/database name'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/parking_lot'
db=SQLAlchemy(app)


class Test(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/usersignup")
def usersignup():
    return render_template("usersignup.html")


@app.route("/userlogin")
def userlogin():
    return render_template("userlogin.html")

























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
