# CSE 460 Project: Recipe Generator
Recipe generator using a subset of data from RecipeNLG dataset(http://recipenlg.cs.put.poznan.pl/).
Using Select2 to choose a subset of ingredients to find existing recipes.
Following the tutorial for flask and postgresql setup: https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/


Setting Up With Windows:
```
npm install -g bower
pip install pipenv
pipenv install flask psycopg2
```


Setting Up With Mac OS:
```
python3 -m venv venv
source venv/bin/activate
pip install psycopg2-binary==2.9.2
pip install flask
```

run:
python3 app.py
http://127.0.0.1:5000/

# IMPORTANT 
```
1. Run -> python3 app.py (Please make sure pgadmin is open)
    - This setups all the tables, table modifications, trigger and view.
2. Comment out lines 70-77 from database/databaseModule.py 
    - Disables the creation of triggers, views and modifications from being ran again.
3. After the above steps are done you are free to run the application normally with 
```
