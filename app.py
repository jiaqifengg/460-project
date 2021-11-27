from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_select2 import Select2

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cse460db'
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('templates/static/home.html')

@app.route('/recipes')
def find_recipes():
    ingredients = request.form.getlist('ingredients')
    print(ingredients)

if __name__ == "__main__":
    app.debug = True
    app.run()