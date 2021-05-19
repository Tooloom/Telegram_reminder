"""
Master class for work with pymysql. Here have:
Creation new table
Execute query with return
Execute query without return
"""
import pymysql

import config


class WorkDB():
    """Master class for work with database"""
    def __init__(self, table, cols, with_create=True):
        self.db = config.DB
        self.username = config.LOGIN
        self.password = config.PASSWORD
        self.host = config.HOST
        self.table = table
        self.cols = cols

        if with_create:
            self._create_table()

    def __connect(self):
        connect = pymysql.connect(
            db=self.db,
            host=self.host,
            user=self.username,
            password=self.password
            )
        return connect

    def _execute_query_without_return(self, *queryes):
        connect = self.__connect()
        try:
            with connect.cursor() as cursor:
                for query in queryes:
                    cursor.execute(query)
        finally:
            connect.commit()
        connect.close()

    def _execute_query_with_return(self, query):
        connect = self.__connect()
        try:
            with connect.cursor() as cursor:
                cursor.execute(query)
                query_data = cursor.fetchall()
        finally:
            connect.commit()
        connect.close()
        return query_data

    def _create_table(self):
        query = f"CREATE TABLE IF NOT EXISTS {self.table} {self.cols} "\
            "CHARACTER SET utf8 COLLATE utf8_general_ci;"

        self._execute_query_without_return(query)
