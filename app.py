from flask import Flask, render_template, request, redirect, url_for, make_response
from database.databaseModule import database
from auth import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cse460pw@localhost/cse460db'
db = database(app)

@app.route('/', methods=['GET'])
def index():

    # get the token
    token = request.cookies.get('id')
    #print(db.check_token(token))

    ## when insert comment 
    # check if userid and recipeid exist
    userid = 4
    recipeid = 102
    comment = 'hello'
    if db.check_recipeid_userid_exist(userid, recipeid):
        # check if comment is empty
        if comment != '':
            db.insert_comment(userid, recipeid, comment)

    #print(db.get_comment_by_recipe_id(100))


    # recipeid_generator
    ingredient = ["Tofu", "Beef"]
    print(db.recipeid_generator(ingredient))

    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')

        if db.check_user_exist(username):

            token = authentication_generator()
            if db.login(username, password,token):
                respone = make_response('log in successfully')
                respone.set_cookie('id', token)
                return respone
            else:
                return "Please enter the correct password."        
        else:
            return 'Username does not exist.'

    return render_template('login.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    msg = "Register successfully."

    token = request.cookies.get('id')
    print(token)

    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        # vaild password: 12345asdfASD!

        username = request.form.get('username')
        password = request.form.get('password')

        # check if the username exist
        if db.check_user_exist(username):
            return 'Username already exists.'

        # check username
        check_username = username_vaild(username)
        if not check_username[0]:
            return check_username[1]
            
        # check password
        check_password = password_vaild(password)
        if not check_password[0]:
            return check_password[1]
        
        # successfully register
        # store username and password in database
        db.register(username, password)
        return "Register successfully."
        
    return render_template('register.html')


@app.route('/recipes')
def find_recipes():
    ingredients = request.args.getlist('ingredients')
    print(ingredients)
    recipe_list = db.get_recipes(ingredients)
    amount = len(recipe_list)
    # recipe_list = ['1', '2', '3']
    return render_template('recipeList.html', total_recipes=amount, recipe_list=recipe_list)


@app.route('/recipe/<id>', methods=['GET'])
def recipe(id):
    the_recipe = db.get_recipe_by_id(id)
    title = the_recipe[1]
    ingredients_amount = the_recipe[2]
    directions = the_recipe[3]
    source = the_recipe[4]
    the_id = the_recipe[0]
    comments = db.get_comment_by_recipe_id(the_id)
    print(the_recipe)
    return render_template('recipe.html', title=title, 
                            ingredients_list=ingredients_amount, 
                            directions_list=directions, original=source, id=the_id)

@app.route('/comment/<id>', methods=['POST'])
def submit_comment(id):
    pass


if __name__ == "__main__":
    app.debug = True
    app.run()