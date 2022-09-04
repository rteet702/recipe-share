import email
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import re


NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9!@#$%^&*()-_+]{8,}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:

    """
    This class represents a typical user. All methods inside this class will pertain to the User, as well as any related data.
    Tentatively, this class will be set up to handle the storing of 'Recipe' instances.
    """

    def __init__(self, data:dict) -> None:
        self.id = data.get('id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.email = data.get('email')
        self.password = data.get('password')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.recipes = []

    @staticmethod
    def register_user(data:dict) -> None:
        """Pick up data from the user submitted form, and insert it into a database."""

        query = """INSERT INTO users (first_name, last_name, email, password)
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def validate_registration(form:dict) -> bool:
        """Validates the registration form submitted by the user when creating an account."""

        is_valid = True

        email_data = {'email': form.get('email_registration')}

        if User.get_by_email(email_data) is not [] or ():
            is_valid = False
        if not EMAIL_REGEX.match(form.get('email_registration')):
            is_valid = False
        if not NAME_REGEX.match(form.get('first_name')):
            is_valid = False
        if not NAME_REGEX.match(form.get('last_name')):
            is_valid = False
        if not PASSWORD_REGEX.match(form.get('password_registration')):
            is_valid = False
        if form.get('password_registration') != form.get('password_confirmation'):
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(form:dict) -> bool:
        """Validates the login form submitted by the user."""

        is_valid = True

        email_data = {'email': form.get('email_login')}

        if not User.get_by_email(email_data):
            is_valid = False
        return is_valid
    @classmethod
    def get_by_email(cls, data:dict):
        """Check if there is an user associated with the provided email. If a user is found, returns an object constructed from the query."""

        query = "SELECT * FROM users WHERE email=%(email)s;"
        result = connectToMySQL('recipes').query_db(query, data)
        if result == () or result == []:
            return False
        else:
            return cls(result[0])