from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import store_model
from flask_app.models import user_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'shopping_list_app'

class Items:
    def __init__(self, data):
        self.id = data['id']
        self.updated_at = data['created_at']
        self.created_at = data['updated_at']
        self.item_name = data['item_name']
        self.price = data['price']
        self.store_id = data['store_id']
        self.store_user_id = data['store_user_id']
        self.items = []
        self.user = []
        self.store = []
        #follow database table fields plus any other attribute you want to create
        pass

    @classmethod
    def get_items_w_stores(cls):
        query = "SELECT * FROM items JOIN store ON store.id = store_id;"
        results = connectToMySQL(db).query_db(query)
        print(query)
        print(results)
        return results
    
    @classmethod
    def get_items_one_store(cls, id):
        query="SELECT * FROM store LEFT JOIN items ON store.id = store.id WHERE store.id =%(id)s;"
        results = connectToMySQL(db).query_db(query,{'id': id})
        #results = connectToMySQL(db).query_db(query)
        print(query)
        one_store = cls(results[0])
        print("one car, filtered!", one_store)
        print("UNFILTERED!!!!!", results)
        print("--------------", one_store)
        return results[0]
        #may need to comment out lines 39-43 and just return results with no filtering

    @classmethod
    def save_item(cls,data):
        query = "INSERT INTO shopping_list_app.items (id,created_at, updated_at, item_name, price,store_id, store_user_id) VALUES (DEFAULT,  NOW(), NOW(), %(item_name)s, %(price)s, %(store_id)s, %(store_user_id)s;"
        return connectToMySQL("shopping_list_app").query_db(query, data)
    
    @classmethod
    def update_item(cls, data):
        query = "UPDATE items SET created_at=NOW(), updated_at=NOW(), item_name=%(item_name)s, price=%(price)s, store_id=%(store_id)s, store_user_id=%(store_user_id)s  WHERE id =%(id)s;"
        print(query)
        results = connectToMySQL("shopping_list_app").query_db(query,data)
        return results
    
    @classmethod
    def get_one_item(cls,id):
        query = "SELECT * FROM items WHERE id = %(id)s;"
        results = connectToMySQL('shopping_list_app').query_db(query,{"id":id})
        print("RRRREEEEEEESSSSSSSSUUULLLTTTSS", results)
        one_item = results[0]
        print("ONE CAR!", one_item)
        return one_item
    
    @staticmethod
    def validate_items(items):
        is_valid = True
        print("#############################################")
        if len(items['item_name']) < 3:
            flash("Item name must be at least 3 characters!!")
            is_valid = False
        if len(items['price']) <= 0:
            flash("Make must be at least 0!!")
            is_valid = False
        return is_valid
    
    @classmethod
    def delete_item(cls, id):
        query  = "DELETE FROM items WHERE id = %(id)s;"
        result = connectToMySQL('shopping_list_app').query_db(query, id)
        return result