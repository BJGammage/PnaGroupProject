from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import store_model
from flask_app import items_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#might need other imports like flash other classes and regex

db = 'shopping_list_app'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['updated_at']
        self.updated_at = data['created_at']
        self.email = data['email']
        self.password = data['password']
        self.store= []
        self.items= []
        #follow database table fields plus any other attribute you want to create
        pass


    @classmethod
    def rename(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(db).query_db(query)
        #Nice little head start
        #Rest of code here
        print(results)
        return "Something here"
    
    @classmethod
    def allUsers(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(db).query_db(query)
        print(results)
        return results
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO user (id, created_at, updated_at, email, password ) VALUES (DEFAULT, NOW(), NOW(), %(email)s, %(password)s);"
        return connectToMySQL("car_dealz").query_db(query, data)
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        print("#############################################")
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email/password address!")
            is_valid = False
            # return is_valid
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords must match")
            is_valid = False
        return is_valid
    
    @classmethod
    def find_User(cls, email_dict):
        query = "SELECT * from user WHERE email = %(email)s"
        db_response = connectToMySQL(db).query_db(query, email_dict)
        print(db_response)
        if len(db_response) < 1:
            return False
        return db_response
    
    @classmethod
    def find_User2(cls, email_dict):
        query = "SELECT * from user WHERE email = %(email)s"
        db_response = connectToMySQL(db).query_db(query, email_dict)
        print(db_response)
        if len(db_response) < 1:
            return False
        return cls(db_response[0])