from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        results = connectToMySQL('recipes').query_db(query)
        users = []

        for user in results:
            users.append ( cls(user))
        return users
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def check_existing_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        if len(results) > 0:
            return True
        return False

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"

        return connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if(len(user['first_name'])) < 2:
            flash("First name must be longer than 2 characters", "first_name")
            is_valid = False
        if(len(user['last_name'])) < 2:
            flash("Last name must be longer than 2 characters", "last_name")
            is_valid = False
        if(len(user['email'])) < 2:
            flash("Email must be longer than 2 characters", "email")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email Address', 'email')
            is_valid = False
        
        if(len(user['password'])) < 2:
            flash("Password must be longer than 8 characters", "password")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords must match", "confirm_password")
            is_valid = False
        return is_valid
    