from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def create(cls,data):

        data['password']=bcrypt.generate_password_hash(data['password']) 

        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        return connectToMySQL("recipes").query_db(query,data)

    @classmethod
    def find_by_email(cls, data):

        query="SELECT * FROM users WHERE email=%(email)s"
        result=connectToMySQL("recipes").query_db(query,data)

        if len(result) > 0:
            return cls(result[0])
        else:
            return False

    @staticmethod
    def validate_register(data):
        is_valid=True
        query="SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL("recipes").query_db(query,data)
        if len(results) >= 1:
            flash('Email already taken. Please try another one')
            is_valid=False
        if len(data['first_name'])<2:
            flash("First Name must be at least 2 characters")
            is_valid=False
        if len(data['last_name'])<2:
            flash("Last Name must be at least 2 characters")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address")
            is_valid=False
        if len(data['password'])<8:
            flash("Password must be at least 8 characters")
            is_valid=False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match!")
            is_valid=False

        return is_valid

    @staticmethod
    def validate_login(data):

        found_user = User.find_by_email(data)
        if found_user:
            if bcrypt.check_password_hash(found_user.password, data['password']):
                return True
            else:
                flash("Invalid Login.")
                return False
        else:
            flash("Invalid Login.")

    @classmethod
    def find_by_id(cls, data):

        query="SELECT * FROM users WHERE email=%(id)s"
        result=connectToMySQL("recipes").query_db(query,data)

        if len(result) > 0:
            return cls(result[0])
        else:
            return False