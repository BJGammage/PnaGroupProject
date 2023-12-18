from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model
from flask_app.models import items_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'shopping_list_app'

class Store:
    def __init__(self, data):
        self.id = data['id']
        self.updated_at = data['created_at']
        self.created_at = data['updated_at']
        self.store_name = data['store_name']
        self.location = data['location']
        self.price = data['price']
        self.user_id = data['user_id']
        self.user = []
        self.store = []
        self.items = []
        #follow database table fields plus any other attribute you want to create
        pass

    @classmethod
    def get_stores_w_users(cls):
        query = "SELECT * FROM store JOIN user ON store.user_id = user.id;"
        results = connectToMySQL(db).query_db(query)
        print(query)
        print(results)
        return results
    
    @classmethod
    def get_one_store_one_user(cls, id):
        
        query="SELECT * FROM store JOIN user ON store.user_id = user.id WHERE store.id = %(id)s;"
        results = connectToMySQL(db).query_db(query,{'id': id})
        print(query)
        one_car = cls(results[0])
        print("one car, filtered!", one_car)
        print("UNFILTERED!!!!!", results)
        print("------", one_car)
        return results[0]
    
    @classmethod
    def save_store(cls,data):
        query = "INSERT INTO shopping_list_app.store (id, created_at, updated_at, store_name, location, user_id) VALUES (DEFAULT, NOW(), NOW(), %(store_name)s, %(location)s,%(user_id)s);"
        return connectToMySQL("shopping_list_app").query_db(query, data)
    
    @classmethod
    def update_store(cls, data):
        query = "UPDATE store SET created_at=NOW(), updated_at=NOW(), store_name=%(store_name)s, location=%(location)s, WHERE id =%(id)s;"
        print(query)
        results = connectToMySQL("shopping_list_app").query_db(query,data)
        return results
    
    @classmethod
    def get_one_store(cls,id):
        query = "SELECT * FROM store WHERE id = %(id)s;"
        results = connectToMySQL('shopping_list_app').query_db(query,{"id":id})
        print("RRRREEEEEEESSSSSSSSUUULLLTTTSS", results)
        one_store = results[0]
        print("ONE STORE!", one_store)
        return one_store
    
    @staticmethod
    def validate_store(store):
        is_valid = True
        print("#############################################")
        if len(store['store_name']) < 3:
            flash("Store name must be at least 3 characters!!")
            is_valid = False
        if len(store['location']) < 3:
            flash("Location must be at least 3 characters!!")
            is_valid = False
        return is_valid
    
    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM store WHERE id = %(id)s;"
        result = connectToMySQL('shopping_list_app').query_db(query, id)
        return result