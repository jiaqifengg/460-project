import psycopg2
from database.dbconfig import config


class database():
    def __init__(self, app):
        #database_url = engine + '://' + user + ':' + password + '@' + host + '/' + dbname
        #app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        #self.db = SQLAlchemy(app)
        #sql = ("CREATE TABLE IF NOT EXISTS animals (id SERIAL PRIMARY KEY, name VARCHAR(160) UNIQUE);")
        #self.db.engine.execute(sql)

        connection = psycopg2.connect(user = config.user,
                            password = config.password,
                            host = config.host,
                            dbname = config.dbname)
        cursor = connection.cursor()

        # create user table
        create_user_table = """CREATE TABLE IF NOT EXISTS users(
                                userid SERIAL NOT NULL,
                                username VARCHAR(50) NOT NULL,
                                password VARCHAR(50) NOT NULL,
                                logged_token VARCHAR(512) DEFAULT NULL,
                                PRIMARY KEY (userid, username)
                            );"""
        cursor.execute(create_user_table)

        # insert userid 0 refer to administrator
        insert_0 = "INSERT INTO users (username, password) VALUES ('Administrator', 'cse460temp')"
        cursor.execute(insert_0)

        # create recipe talbe
        recipe_table = """CREATE TABLE IF NOT EXISTS recipes(
                            recipeid SERIAL NOT NULL PRIMARY KEY,
                            title TEXT NOT NULL,
                            ingredients TEXT[] NOT NULL,
                            directions TEXT[],
                            from_link TEXT,
                            from_source TEXT,
                            ner TEXT[]
                        );"""
        # when insert need to be a arrary form https://www.postgresqltutorial.com/postgresql-array/
        cursor.execute(recipe_table)
        # add
        # drop from_source 
        # rename ingredients to ingredients_amount
        # add userid 
        # rename ner to ingredients


        # create comment table
        # make sure to check the comment is not empty when insert 
        comment_table = """CREATE TABLE IF NOT EXISTS comments(
                            userid INT,
                            recipe INT,
                            comment TEXT NOT NULL
                        );"""
        # add constrain 
        # userid reference user.userid
        # recipeid reference recipes.recipeid
        cursor.execute(comment_table)
        connection.commit()