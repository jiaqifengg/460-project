import psycopg2
from database.dbconfig import config
import hashlib
import random

# be careful when dropping userid and recipeid 
# when user.userid delete 
# 1) delete all the comment that user make
# 2) change the recipe.userid to 1

# when recipe delete
# delete all the comment with that recipe id

class database():
    def __init__(self):
        

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
                            userid INT,
                            recipeid INT,
                            comment TEXT NOT NULL,
                            FOREIGN KEY (recipeid) REFERENCES recipes(recipeid)
                        );"""
        self.cursor.execute(comment_table)

        # create categories table
        category_table = """CREATE TABLE IF NOT EXISTS categories(
                            category VARCHAR(50) PRIMARY KEY,
                            recipes integer[]
                        );"""
        self.cursor.execute(category_table)

        # import recipes.csv to recipes table 
        # with Header yes and Delimeter ,
        # SET UP HELPER FUNCTIONS SHOULD BE ONLY RUN ONCE AFTER IMPORT RECIPES TABLES
        # uncomment the following helper functions after import and comment once done
        
        # oneTime = True 
        # if oneTime:
        #     oneTime = False
        #     self.set_up_helper1_after_recipes_imported()
        #     self.set_up_helper2_change_administrator()
        #     self.set_up_helper3_fill_category_table()
        #     self.set_up_helper4_create_view_category_count()
        #     self.set_up_helper5_trigger_for_comment()

        self.connection.commit()


    def set_up_helper1_after_recipes_imported(self):
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
    

    def set_up_helper2_change_administrator(self):
        # hash the password of administrator
        hash_admin_password = hash_function('cse460temp')

        # change the length of char password can hold
        extend_password_len = """ALTER TABLE users ALTER COLUMN password TYPE character varying(512);"""
        self.cursor.execute(extend_password_len)
        self.connection.commit()

        # update the password of administrator
        update_admin_password = """UPDATE users 
                                SET password=(%s) 
                                WHERE username = 'Administrator';"""
        val = (hash_admin_password, )
        self.cursor.execute(update_admin_password, val)
        self.connection.commit()


    def set_up_helper3_fill_category_table(self):

        #Creates an array of recipes containing chicken, and then inserts into the categories table
        chicken = "select recipeid from recipes where CONCAT(',', ingredients, ',') like '%,chicken,%'"
        self.cursor.execute(chicken)
        chickenArray = self.cursor.fetchall()
        insert_chicken = "INSERT INTO categories (category, recipes) VALUES ('Chicken', %s);"
        self.cursor.execute(insert_chicken, (chickenArray,))

        #Creates an array of recipes containing beef, and then inserts into the categories table
        beef = "select recipeid from recipes where CONCAT(',', ingredients, ',') like '%,beef,%'"
        self.cursor.execute(beef)
        beefArray = self.cursor.fetchall()
        insert_beef = "INSERT INTO categories (category, recipes) VALUES ('Beef', %s);"
        self.cursor.execute(insert_beef, (beefArray,))

        #Creates an array of recipes containing fish, and then inserts into the categories table
        fish = "select recipeid from recipes where CONCAT(',', ingredients, ',') like '%,fish,%'"
        self.cursor.execute(fish)
        fishArray = self.cursor.fetchall()
        insert_fish = "INSERT INTO categories (category, recipes) VALUES ('Fish', %s);"
        self.cursor.execute(insert_fish, (fishArray,))

        #Creates an array of recipes containing pork, and then inserts into the categories table
        pork = "select recipeid from recipes where CONCAT(',', ingredients, ',') like '%,pork,%'"
        self.cursor.execute(pork)
        porkArray = self.cursor.fetchall()
        insert_pork = "INSERT INTO categories (category, recipes) VALUES ('Pork', %s);"
        self.cursor.execute(insert_pork, (porkArray,))

        #Creates an array of recipes containing tofu, and then inserts into the categories table
        tofu = "select recipeid from recipes where CONCAT(',', ingredients, ',') like '%,tofu,%'"
        self.cursor.execute(tofu)
        tofuArray = self.cursor.fetchall()
        insert_tofu = "INSERT INTO categories (category, recipes) VALUES ('Tofu', %s);"
        self.cursor.execute(insert_tofu, (tofuArray,))


    def set_up_helper4_create_view_category_count(self):
        sql = """CREATE VIEW category_count AS
                SELECT category, cardinality(recipes)
                FROM categories
                GROUP BY category
                ORDER BY cardinality(recipes) DESC"""
        
        self.cursor.execute(sql)
        self.connection.commit()
        return 


    def set_up_helper5_trigger_for_comment(self):
        # drop all userid foreign key for recipeid

        sql = "ALTER TABLE recipes DROP CONSTRAINT recipe_userid_reference_user;"
        self.cursor.execute(sql)
        self.connection.commit()
        
        function = """CREATE OR REPLACE FUNCTION userid_delete() RETURNS TRIGGER AS 
                        $BODY$
                        BEGIN
                            DELETE FROM comments
                            WHERE comments.userid=OLD.userid;
                            RETURN NULL;
                        END;
                        $BODY$
                        language plpgsql;"""
        self.cursor.execute(function)


        sql = """CREATE trigger useid_check
                AFTER DELETE ON users
                FOR EACH ROW 
                EXECUTE PROCEDURE userid_delete();"""
        
        self.cursor.execute(sql)
        self.connection.commit()
        return 
    


    def check_user_exist(self, username):
        sql = """SELECT userid 
                FROM users 
                WHERE username=%s;"""
        val = (username,)
        self.cursor.execute(sql, val)
        myresult = self.cursor.fetchall()

        if len(myresult) == 0:
            return False
        return True
   

    def register(self, username, password): 
        # make sure to check if the username exist before using this function
        sql = "INSERT INTO users (username, password)"
        sql += "VALUES (%s, %s)"
        hashed_password = hash_function(password)
        val = (username, hashed_password)
        self.cursor.execute(sql, val)
        self.connection.commit()


    def login(self, username, password, token):
        # make sure to check if the username exist before using this function        
        sql = "SELECT password FROM users WHERE username=(%s);"
        val = (username, )
        self.cursor.execute(sql, val)
        hashed_password = self.cursor.fetchall()[0][0]

        # check if the password is correct
        if hash_function(password) == hashed_password:
            # update token
            sql = """UPDATE users
                    SET logged_token=%s
                    WHERE username=%s;"""
            hash_token = hash_function(token)
            val = (hash_token, username)
            self.cursor.execute(sql, val)
            self.connection.commit()
            return True

        return False

    def delete_account(self, username):
        # check token first
        sql = "DELETE FROM users where username=%s"
        val = (username,)
        self.cursor.execute(sql, val)
        self.connection.commit()

        
    def check_token(self, token):
        # return [] when the token is not exist
        # return [id, username] when token is exist
        # check if token exist
        if token == None:
            return []
        
        hash_token = hash_function(token)
        sql = """SELECT userid, username
                FROM users
                WHERE logged_token=(%s)"""
        val = (hash_token,)
        self.cursor.execute(sql,val)
        user = self.cursor.fetchall()

        # when there is no token match with the input token
        if len(user) == 0:
            return []
        
        return user[0]

    def get_recipes(self, ingredient_list):
        query = """SELECT * FROM recipes WHERE %s && ingredients"""
        # print(query % ingredient_list)
        self.cursor.execute(query, (ingredient_list,))
        results = self.cursor.fetchall()
        self.connection.commit()
        ids_title = []
        for recipe in results:
            id = recipe[0]
            title = recipe[1]
            ids_title.append((id, title))
        # print(ids_title)
        return ids_title
        
    def check_recipeid_userid_exist(self, userid, recipeid):
        if type(userid) == int and type(recipeid) == int:
            # check if the userid exists
            sql = """SELECT userid
                    FROM users
                    WHERE userid="""
            self.cursor.execute(sql + str(userid))
            userid = self.cursor.fetchall()
            if len(userid) == 0:
                return False
            
            # check if the recipeid exists
            sql = """SELECT recipeid
                    FROM recipes
                    WHERE recipeid="""
            self.cursor.execute(sql + str(recipeid))
            recipeid = self.cursor.fetchall()
            if len(userid) == 0:
                return False
            return True       
        return False

    def insert_comment(self, userid, recipeid, comment):
        sql = """INSERT INTO comments (userid, recipeid, comment)
                    VALUES (%s, %s, %s)"""
        val = (userid, recipeid, comment)
        self.cursor.execute(sql, val)
        self.connection.commit()
        
    def get_comment_by_recipe_id(self, recipeid):
        # return [(username, comment), (username, comment)....] 
        
        sql = """SELECT userid, comment
                    FROM comments
                    WHERE recipeid=%s"""
        val = (recipeid,)
        self.cursor.execute(sql, val)
        comments = self.cursor.fetchall()
        print(comments)
        if len(comments) == 0:
            return []

        else:
            length = len(comments)
            for i in range(0, length):
                sql = "SELECT username FROM users WHERE userid=%s"
                userid = comments[i][0]
                print(userid)
                self.cursor.execute(sql, (userid,))
                result = self.cursor.fetchall()
                print(result)
                if len(result) == 0:
                    return []
                else:
                    username = result[0][0]
                    result_tuple = (username, comments[i][1])
                    comments[i] = result_tuple
        return comments

    
    def recipeid_generator(self, list_of_food):
        # using subqueries for union
        # input has to be ["Beef", "Chicken", "Fish", "Pork", "Tofu"]
        resut = 0 # when there is no correct result 

        sql = """SELECT recipes
                    FROM categories
                    WHERE category=%s """

        sql_format = """SELECT recipes
                    FROM categories
                    WHERE category=%s """
        
        val = (list_of_food[0],)
        for i in range(1, len(list_of_food)):
            sql += "UNION "
            sql += sql_format
            val = val + (list_of_food[i],)
        
        self.cursor.execute(sql, val)
        recipes = self.cursor.fetchall()

        if len(recipes) > 0:
            recipes_list = []
            for i in recipes:
                recipes_list += i[0]

            result = random.choice(recipes_list)

            return result

    def get_recipe_by_id(self, id):
        query = """SELECT * FROM recipes WHERE recipeid=%s"""
        vals = (id,)
        self.cursor.execute(query, vals)
        reuslts = self.cursor.fetchall()
        self.connection.commit()
        return reuslts[0]


    def get_category_count(self):
        query = "SELECT * FROM category_count"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.connection.commit()
        return result


    def update_password(self, userid, username, curr_pw, new_pw):
        user_exist = self.check_user_exist(username)
        if user_exist:
            hashed_curr_pw = hash_function(curr_pw)
            hashed_new_pw = hash_function(new_pw)
            query = """SELECT * FROM users WHERE userid=%s"""
            self.cursor.execute(query, (userid,))
            results = self.cursor.fetchall()
            self.connection.commit()
            stored_pw = results[0][2]
            if hashed_curr_pw == stored_pw:
                update_query = "UPDATE users SET password=%s WHERE userid=%s"
                vals = (hashed_new_pw, userid)
                self.cursor.execute(update_query, vals)
                self.connection.commit()
                return [True, 'Password Successfully Changed!']
            else:
                return [False, 'Please Input the Correct Current Password']
        else:
            return [False, 'User does not exist with such username']
    
    


def hash_function(input):
    new_pw = input.encode()
    hash_input = hashlib.sha256(new_pw).hexdigest()
    return hash_input
    




        