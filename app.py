from ctypes import resize
from flask import Flask, render_template, request, redirect, url_for, make_response
from werkzeug.wrappers import Response, response
from database.databaseModule import database
from auth import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cse460pw@localhost/cse460db'
db = database(app)

@app.route('/', methods=['GET'])
def index():

    # get the token
    token = request.cookies.get('id')
    auth = False
    if db.check_token(token) != []:
        auth = True
    #print(db.check_token(token))
    count_category = db.get_category_count()
    print(count_category)
    chicken_count = str(count_category[0][1])
    pork_count = str(count_category[1][1])
    beef_count = str(count_category[2][1])
    fish = str(count_category[3][1])
    tofu = str(count_category[4][1])
    ## when insert comment 
    # check if userid and recipeid exist
    # userid = 4
    # recipeid = 102
    # comment = 'hello'
    # if db.check_recipeid_userid_exist(userid, recipeid):
    #     # check if comment is empty
    #     if comment != '':
    #         db.insert_comment(userid, recipeid, comment)

    return render_template('home.html', auth=auth, chicken_count=chicken_count, pork_count=pork_count, beef_count=beef_count, fish_count=fish, tofu_count=tofu)


@app.route('/login', methods=['GET', 'POST'])
def login():
    token = request.cookies.get('id')
    if db.check_token(token) != []: # no access to /register
        return 'You are already logged in!'

    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')

        if db.check_user_exist(username):

            token = authentication_generator()
            if db.login(username, password, token):
                respone = make_response('log in successfully')
                respone.set_cookie('id', token)
                return respone
            else:
                return "Please enter the correct password."        
        else:
            return 'Username does not exist.'

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    token = request.cookies.get('id')
    if db.check_token(token) != []:# no access to /register
        return 'You are already registered'

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
    token = request.cookies.get('id')
    auth = False
    if db.check_token(token) != []:
        auth = True
    ingredients = request.args.getlist('ingredients')
    recipe_list = db.get_recipes(ingredients)
    amount = len(recipe_list)
    # recipe_list = ['1', '2', '3']
    return render_template('recipeList.html', total_recipes=amount, recipe_list=recipe_list, auth=auth)


@app.route('/recipe/<id>', methods=['GET'])
def recipe(id):
    token = request.cookies.get('id')
    auth = False
    # if there is not a cookie then they cannot submit a comment
    if db.check_token(token) != []:
        auth = True
    the_recipe = db.get_recipe_by_id(id)
    # print(the_recipe)
    title = the_recipe[1]
    ingredients_amount = the_recipe[2]
    directions = the_recipe[3]
    # print(source)
    recipe_id = the_recipe[0]
    print(recipe_id)
    comments = db.get_comment_by_recipe_id(recipe_id)
    print(comments)
    template = render_template('recipe.html', title=title, 
                            ingredients_list=ingredients_amount, 
                            directions_list=directions, id=recipe_id, comments_list=comments, auth=auth)

    return make_respond_with_cookie(recipe_id, template)


@app.route('/comment', methods=['POST'])
def submit_comment():
    comment = request.form['submit-comment']
    print("Here")
    print(comment)
    token = request.cookies.get('id')
    data = db.check_token(token)
    userid = data[0]
    recipe_id = request.cookies.get('recipeid')
    db.insert_comment(userid, recipe_id, comment)
    return redirect('/recipe/%s' % str(recipe_id))
    
@app.route('/randomRecipe')
def generate_random_recipe():
    categories = request.args.getlist('category')
    recipe_id = db.recipeid_generator(categories)
    print(categories)
    print(recipe_id)
    return redirect('/recipe/%s' % str(recipe_id))

def make_respond_with_cookie(recipeid, template):
    response = make_response(template)
    response.set_cookie('recipeid', str(recipeid).encode('utf-8'))

    return response

@app.route('/settings')
def settings():
    token = request.cookies.get('id')
    data = db.check_token(token)
    # if there is not a cookie then they cannot submit a comment
    if data == []:
        return '403 Forbidden - Please Login'
    else:
        return render_template('settings.html')

@app.route('/password', methods=['POST'])
def passwordChange():
    token = request.cookies.get('id')
    data = db.check_token(token)
    if data == []:
        return '403 Forbidden'
    else:
        userid = data[0]
        username = data[1]
        curr_pw = request.form.get('curr-pw')
        new_pw = request.form.get('new-pw')
        check_password = password_vaild(new_pw)
        if not check_password[0]:
            return check_password[1]
        else:
            results = db.update_password(userid, username, curr_pw, new_pw)
            return results[1]

@app.route('/delete_account')
def delete_account():
    token = request.cookies.get('id')
    _ = db.check_token(token)
    if _ != []:
        username = _[1]
        db.delete_account(username)
        return redirect('/')
        # return to main page
    else:
        return "403 Response"
    


    
        
    
if __name__ == "__main__":
    app.debug = True
    app.run()