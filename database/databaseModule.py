class database:
    def __init__(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cse460db'