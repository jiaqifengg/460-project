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
        create_user_talbe = "CREATE TABLE IF NOT EXISTS users( "
        create_user_talbe += "userid SERIAL NOT NULL, "
        create_user_talbe += "username VARCHAR(50) NOT NULL, "
        create_user_talbe += "password VARCHAR(50) NOT NULL, "
        create_user_talbe += "hash_token_in_binary BYTEA DEFAULT NULL, "
        create_user_talbe += "PRIMARY KEY (userid, username)"
        create_user_talbe += ");"
        cursor.execute(create_user_talbe)

        # insert userid 0 refer to administrator
        insert_0 = "INSERT INTO users (username, password) "
        insert_0 += "VALUES ('Administrator', 'cse460temp')"
        cursor.execute(insert_0)

        # create recipe talbe
        recipe_table = "CREATE TABLE IF NOT EXISTS recipes( "
        recipe_table += "recipeid SERIAL NOT NULL PRIMARY KEY, "
        recipe_table += "title TEXT NOT NULL, "
        recipe_table += "ingredients TEXT NOT NULL, "
        # when insert need to be a arrary form https://www.postgresqltutorial.com/postgresql-array/
        recipe_table += "directions TEXT[], "
        recipe_table += "from_link TEXT, "
        recipe_table += "from_source TEXT,"
        recipe_table += "ner TEXT[]"
        recipe_table += ");"
        cursor.execute(recipe_table)
        # add
        # drop from_source 
        # rename ingredients to ingredients_amount
        # add userid 
        # rename ner to ingredients


        # create comment table
        # make sure to check the comment is not empty when insert 
        comment_talbe = "CREATE TABLE IF NOT EXISTS comments( "
        comment_talbe += "userid INT, "
        comment_talbe += "recipeid INT, "
        comment_talbe += "comment TEXT NOT NULL "
        comment_talbe += ");"
        # add constrain 
        # userid reference user.userid
        # recipeid reference recipes.recipeid
        cursor.execute(comment_talbe)


        connection.commit()