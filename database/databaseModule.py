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
        sql = "CREATE TABLE IF NOT EXISTS animals (id VARCHAR(10) PRIMARY KEY, name VARCHAR(160) UNIQUE);"
        cursor.execute(sql)
        connection.commit()