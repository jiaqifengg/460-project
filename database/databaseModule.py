import psycopg2
import csv
from database.dbconfig import config

# be careful when dropping userid and recipeid 
# when user.userid delete 
# 1) delete all the comment that user make
# 2) change the recipe.userid to 1

# when recipe delete
# delete all the comment with that recipe id

class database():
    def __init__(self, app):
        #database_url = engine + '://' + user + ':' + password + '@' + host + '/' + dbname
        #app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        #self.db = SQLAlchemy(app)
        #sql = ("CREATE TABLE IF NOT EXISTS animals (id SERIAL PRIMARY KEY, name VARCHAR(160) UNIQUE);")
        #self.db.engine.execute(sql)
        

        self.connection = psycopg2.connect(user = config.user,
                            password = config.password,
                            host = config.host,
                            dbname = config.dbname)
        self.cursor = self.connection.cursor()

        # create user table
        create_user_table = """CREATE TABLE IF NOT EXISTS users(
                                userid SERIAL PRIMARY KEY,
                                username VARCHAR(50) NOT NULL UNIQUE,
                                password VARCHAR(50) NOT NULL,
                                logged_token VARCHAR(512)
                            );"""
        self.cursor.execute(create_user_table)

        # create recipe talbe
        recipe_table = """CREATE TABLE IF NOT EXISTS recipes(
                            recipeid SERIAL PRIMARY KEY,
                            title TEXT NOT NULL,
                            ingredients TEXT[] NOT NULL,
                            directions TEXT[],
                            from_source TEXT DEFAULT NULL,
                            from_link TEXT,
                            ner TEXT[]
                        );"""
        self.cursor.execute(recipe_table)

        # import csv file

        # create comment table
        # make sure to check the comment is not empty when insert 
        # create trigger
        comment_table = """CREATE TABLE IF NOT EXISTS comments(
                            userid INT UNIQUE,
                            recipeid INT UNIQUE,
                            comment TEXT NOT NULL,
                            FOREIGN KEY (userid) REFERENCES users(userid),
                            FOREIGN KEY (recipeid) REFERENCES recipes(recipeid)
                        );"""
        self.cursor.execute(comment_table)

        # uncomment this function after you imported the recipe
        # import recipes.csv to recipes table 
        # with Header yes and Delimeter ,
        # This FUNCTION SHOULD ONLY RUN ONCE

        # self.after_recipes_imported()
        self.connection.commit()


    def after_recipes_imported(self):
        
        # check if there is 1 inside 
        check_admin_exist = "SELECT userid FROM users WHERE userid=1;"
        self.cursor.execute(check_admin_exist)
        result = self.cursor.fetchall()
        if len(result) == 0:

            # insert userid 1 refer to administrator
            # 1 is administrator 
            insert_1 = "INSERT INTO users (username, password) VALUES ('Administrator', 'cse460temp');"
            self.cursor.execute(insert_1)

        # change recipes table
        alter_recipes = "ALTER TABLE recipes "
        # drop from_link
        drop_from_link = alter_recipes + "DROP COLUMN IF EXISTS from_link;"
        self.cursor.execute(drop_from_link)

        # check if ingredients_amount exist
        #check_ingredient_amount = "SELECT column_name "
        #check_ingredient_amount += "FROM information_schema.columns "
        #check_ingredient_amount += "WHERE table_name='recipes' and column_name='ingredients_amounts';"
        #self.cursor.execute(check_ingredient_amount)
        #print(self.cursor.fetchall())

        # rename ingredients to ingredients_amount
        rename_ingredients_to_ingredients_amount = alter_recipes + "RENAME COLUMN ingredients TO ingredients_amount;"
        self.cursor.execute(rename_ingredients_to_ingredients_amount)

        # rename ner to ingredients
        rename_ner_to_ingredients = alter_recipes + "RENAME COLUMN ner TO ingredients;"
        self.cursor.execute(rename_ner_to_ingredients)

        # add userid
        add_userid_column = alter_recipes + "ADD COLUMN IF NOT EXISTS userid INT NOT NULL DEFAULT 1;"
        self.cursor.execute(add_userid_column)

        # userid reference to user.userid
        userid_foreign_key = alter_recipes
        userid_foreign_key += "ADD CONSTRAINT recipe_userid_reference_user "
        userid_foreign_key += "FOREIGN KEY (userid) "
        userid_foreign_key += "REFERENCES users(userid);"
        self.cursor.execute(userid_foreign_key)

        self.connection.commit()
    
    




        