from flask_app import app 
from flask_app.controllers import shopping_list_app_controller

if __name__=='__main__':
    app.run(debug=True, port=5000)