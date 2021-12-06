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
1. Comment the lines 70-77 from database/databaseModule.py 
    - Disabling modifications until tables are created
2. Run python3 app.py (Please make sure pgadmin is open)
    - This setups the tables only
3. Import the CSV files from project-report\recipes.csv
    - pgadmin -> recipes table RIGHT CLICK -> import recipes.csv 
        - HEADERS YES
        - DELIMETER , 
2. Comment out lines 70-77 from database/databaseModule.py 
    - This enables the modification of the tables, creation of views and triggers.
4. Run python3 app.py (Please make sure pgadmin is open) to run step 2 queries.
5. Comment the lines 70-77 from database/databaseModule.py  
    - Disables the modification of the tables, creation of views and triggers.
3. After the above steps are done you are free to run the application normally with 
```
