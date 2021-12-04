# CSE 460 Project: Recipe Generator
Recipe generator using a subset of data from RecipeNLG dataset(http://recipenlg.cs.put.poznan.pl/).
Using Select2 to choose a subset of ingredients to find existing recipes.

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
