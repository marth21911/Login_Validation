from flask_app import app
from flask import flash 
from flask import render_template, request, redirect, session
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt= Bcrypt(app)

@app.route("/")
def homepage():
    return render_template("logins.html")



@app.route("/create_user", methods= ["POST"])
def create_user():
    # validates if fields have been entered correctly
    if not User.validate_user(request.form):
        return redirect ('/')
    
    #packages form into data
    data = {
        "first_name" : request.form["fname"],
        "last_name" : request.form ["lname"],
        "email" : request.form ["email"],
        "password": request.form ["password"],
        "confirm_pw": request.form ["confirm_pw"]
    }
    
    #validates that passwords match
    if data ["confirm_pw"] != data["password"]:
        flash ("Passwords don't match!")
    
    #should check if email is already used
    if User.get_by_email(data):
        flash ("Email already in use.")
    
    #After all validations, hashes pw for entry
    data ["password"] = bcrypt.generate_password_hash(request.form["password"])
    # and submits data to classmethod new_user
    user_id = User.new_user(data)
    #finally saves id in session
    session["id"]=user_id
    return redirect ("/")

@app.route("/login", methods= ["POST"])
def login():
    data = {
        "email" :request.form ["email"],
        "password" : request.form [ "password"]
    }

    if not User.validate_login(data):
        return redirect ("/")
    user = User.get_by_email(data)
    session["user_id"] = user.id
    return redirect ("/home")

@app.route ("/home")
def home():
    if "user_id" in session:
        data = {
            "id": session["user_id"]
        }
        user = User.get_by_id(data)
    else:
        flash("you aren't logged in!")
        return redirect ("/")
    return render_template("home.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect ("/")