from flask import Flask, render_template, request, redirect, url_for
#from flask_migrate import Migrate
import sys
from database.databaseModule import database
from auth import *
# from flask_wtf import FlaskForm
# from flask_bootstrap import Bootstrap
# from flask_select2 import Select2
# from flask_login import login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cse460pw@localhost/cse460db'
db = database(app)
#migrate = Migrate(app, db)

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')

        if db.check_user_exist(username):
            if db.login(username, password):
                return 'log in successfully'
            else:
                return "Please enter the correct password."        
        else:
            return 'Username does not exist.'



    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = "Register successfully."

    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        # vaild password: 12345asdfASD!

        username = request.form.get('username')
        password = request.form.get('password')

        msg = "Register successfully."
        
        # check if the username exist
        if db.check_user_exist(username):
            msg = 'Username already exists.'
            return msg

        # check username
        check_username = username_vaild(username)
        if not check_username[0]:
            msg = check_username[1]
            return msg
            
        # check password
        check_password = password_vaild(password)
        if not check_password[0]:
            msg = check_password[1]
            return msg
        
        # successfully register
        # store username and password in database
        db.register(username, password)
        
        return msg
        
    return render_template('register.html')


@app.route('/recipes')
def find_recipes():
    ingredients = request.args.getlist('ingredients')
    print("Here", file=sys.stdout)
    print(ingredients, file=sys.stdout)
    recipe_list = ['1', '2', '3']
    return render_template('recipeList.html', recipe_list=recipe_list)

@app.route('/recipe/<id>', methods=['GET'])
def recipe(id):
    print(id)
    return render_template('recipe.html')


if __name__ == "__main__":
    app.debug = True
    app.run()