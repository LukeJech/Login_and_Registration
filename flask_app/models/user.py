
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[\W_]).+$')

class User:
    db = "users_schema" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.birthdate = data['birthdate']
        self.fav_language = data['fav_language']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added her for class association?



    # Create Users Models
    @classmethod
    def create_user(cls, data):
        if not cls.validate_user(data):
            return False
        data = cls.parse_registration_data(data)
        query = """
        INSERT INTO users (first_name, last_name, birthdate, fav_language, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(birthdate)s, %(fav_language)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query, data)
        session['user_id'] = user_id
        session['user_fullname'] = f"{data['first_name']} {data['last_name']}"
        return True

    # Read Users Models
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email}
        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result


    # Update Users Models



    # Delete Users Models

    #Register Validation

    @staticmethod
    def validate_user(user_registration_info):
        is_valid = True
        if len(user_registration_info['first_name']) < 2:
            is_valid = False
            flash("Hey mate, your first name has gotta be at least 2 characters!")
        if len(user_registration_info['last_name']) < 2:
            is_valid = False
            flash("Hey mate, your last name has gotta be at least 2 characters!")
        if not EMAIL_REGEX.match(user_registration_info['email']): 
            is_valid = False
            if user_registration_info['email'] == '':
                flash("Email address cannot be blank.")
                is_valid = False
            elif '@' not in user_registration_info['email']:
                flash("Invalid email address. Missing '@' symbol.")
                is_valid = False
            elif '.' not in user_registration_info['email']:
                flash("Invalid email address. Missing domain extension (ex .com)")
                is_valid = False
            else:
                flash("Invalid email address. Please enter a valid email.")
                is_valid = False
        if User.get_user_by_email(user_registration_info['email'].lower().strip()):
            flash('That email is already in use.')
            is_valid = False
        if not re.match(PASSWORD_REGEX, user_registration_info['password']):
            flash("Password requires at least 1 number and special character")
            is_valid = False
        if len(user_registration_info['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters')
        if user_registration_info['password'] != user_registration_info['confirm_password']:
            is_valid = False
            flash('Passwords did not match')
        if not User.validate_age(user_registration_info['birthdate']):
            is_valid = False
            flash('Sorry you must be 10 years old to register')
        if user_registration_info['conditions'] != 'on':
            flash('You must accept Terms and Conditions')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_age(birthdate):
        current_date = datetime.now().date()
        minimum_age = timedelta(days=365 * 10)  # Minimum age of 10 years
        # Convert birthdate string to a datetime object
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
        if current_date - birthdate >= minimum_age:
            return True
        return False

    @staticmethod
    def parse_registration_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['birthdate'] = data['birthdate']
        parsed_data['fav_language'] = data['fav_language']
        parsed_data['email'] = data['email'].lower().strip()
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data
    
    @staticmethod
    def login_user(data):
        this_user = User.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['user_fullname'] = f"{this_user.first_name} {this_user.last_name}"
                return True
        flash("Yo! That login wasn't correct...")
        return False