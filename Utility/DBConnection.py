import sqlite3


class DBConnection: # Class meant to allow easy usage of a context manager for DB connections
    def __init__(self, host): # Initial method which creates the DB Class
        self.host = host
        self.connection = None

    def __enter__(self): # Enters the context manager and sets the connection
        self.connection = sqlite3.Connection(self.host)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb): # Exits the connection with or without a commit
        if exc_type or exc_type or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()