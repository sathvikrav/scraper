import sqlite3

class PremierDatabase:
    conn = sqlite3.connect('premier_lg.db') # static variable connects to database
    c = conn.cursor()
    tableCreated = False

    @staticmethod
    def create_table():
        print("Table initialized")
        PremierDatabase.c.execute('''CREATE TABLE IF NOT EXISTS latlong
                    (player_name text, player_country text, player_team text, player_assists text, latitude real, longitude real)''') # create a database table if it does not currently exist
        PremierDatabase.conn.commit() # commits changes to sqlite database
        PremierDatabase.tableCreated = True

    @staticmethod
    def insert_player(player_name, player_country, player_team, player_assists, player_lat, player_long):
        print("Player entered into database")
        PremierDatabase.c.execute("INSERT INTO latlong VALUES (?, ?, ?, ?, ?, ?)", (player_name, player_country, player_team, player_assists, player_lat, player_long))
        PremierDatabase.conn.commit()

    @staticmethod
    def select_player(player_name):
        print("Player selected")
        PremierDatabase.c.execute("SELECT * FROM latlong WHERE player_name=?", (player_name,)) # retrieves all information about specific player from table row
        return PremierDatabase.c.fetchone()

    @staticmethod
    def close():
        print("Database connection closed") 
        PremierDatabase.conn.close() # closes the databse connection