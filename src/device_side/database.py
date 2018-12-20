from speech import *
import pymysql #pylint: disable=E0401


class DB:
    """This class handles all database communication"""
    def __init__(self, host="localhost", user="root", password="", database="mysql"):
        self.__connection = None
        self.__cursor = None
        # Only store database (can be used to check if right db, no other vars because security)
        self.__database = database

        self.connect(host, user, password, database)

    def connect(self, host="localhost", user="root", password="", database="mysql"):
        """Sets up connection to the database"""
        self.__connection = pymysql.connect(host, user, password, database)
        self.__cursor = self.get_connection().cursor()

    def get_database(self):
        """Returns database"""
        return self.__database

    def get_connection(self):
        """Returns connection to database"""
        return self.__connection

    def get_cursor(self):
        """Returns cursor of the database"""
        return self.__cursor

    def get(self, table, select = "*", options = "", values=[]):
        """Prepares a get-query"""
        query = "SELECT " + str(select) + " FROM " + \
                str(table) + " " + str(options) + ";" % tuple(values)

        print("GET:", query)

        try:
            self.execute(query)
            self.get_connection().commit()
            return self.get_cursor().fetchall()
        except Exception as exception:
            print("SQL GET EXCEPTION:", exception)
            return False

    def insert(self, table, columns=dict(), values=[]):
        """Prepares an inser-query"""
        query = "INSERT INTO " + str(table) + " (" + str(', '.join(columns.keys())) + \
                ") VALUES (" + str(', '.join(columns.values())) + ");" % tuple(values)

        try:
            self.execute(query)
            self.get_connection().commit()
        except Exception as exception:
            self.get_cursor().rollback()
            print("SQL INSERT EXCEPTION:", exception)
            return False

        return True

    def execute(self, query):
        """ Executes prepared query"""
        self.get_cursor().execute(query)

    def close_connection(self):
        """Closes the connection to the database"""
        self.get_cursor().close()
        self.get_connection().close()
