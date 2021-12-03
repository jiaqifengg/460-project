# https://towardsdatascience.com/sending-data-from-a-flask-app-to-postgresql-database-889304964bf2
# create server group with name: temp 460

# create server
# general -> temp460
# connection -> localhost
# owner -> postgres
# password -> according to what u set for this

class config:
    user = 'postgres'
    password = 'password'
    host = 'localhost'
    dbname = 'cse460db'
