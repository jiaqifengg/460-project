from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
# from flask_wtf import FlaskForm
# from flask_bootstrap import Bootstrap
# from flask_select2 import Select2
# from flask_login import login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cse460pw@localhost/cse460db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    pass

@app.route('/recipes')
def find_recipes():
    ingredients = request.args.getlist('ingredients')
    print("Here", file=sys.stdout)
    print(ingredients, file=sys.stdout)
    return render_template('recipeList.html')

if __name__ == "__main__":
    app.debug = True
    app.run()