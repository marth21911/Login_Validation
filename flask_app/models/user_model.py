from flask_app import app
from flask import  request
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
bcrypt = Bcrypt(app)

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data [ "email"]
        self.password = data[ "password"]
        self.updated_at = data [ "updated_at"]
        self.created_at = data [ "created_at"]
##### MAKE SURE YOU INDENT!
    @staticmethod
    def validate_login(data):
        is_valid = True

        user_in_db = User.get_by_email(data)
        if not user_in_db:
            flash ("Invalid email or password")
            is_valid = False
        if not bcrypt.check_password_hash(user_in_db.password, data["password"]):
            is_valid = False 
        return is_valid



    @staticmethod
    def validate_user(user):
        is_valid = True
        #default is true
        if len(user['fname']) < 3:
            flash ("First name must be at least 3 characters.")
            is_valid = False
            #^ message to front if field has less than 3
        if len(user['lname']) < 3:
            flash ("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash ("Not a valid email.")
            is_valid = False
        if len(user ['password']) < 8:
            flash ("Password must be at least 8 characters.")
            is_valid = False
        if (user['password']) != user['confirm_pw']:
            flash ("Passwords don't match.")
            is_valid = False
        return is_valid

    @classmethod
    def new_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL("users").query_db(query,data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("users").query_db(query, data)
        if len(results) < 1 :
            return False
        return cls(results[0])
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("users").query_db(query, data)
        return cls(results[0])