#!/usr/bin/env python3

import logging
import sqlite3
import sys

class SQLiteDBConnectException(Exception):
    pass

class SQLiteDBExecuteException(Exception):
    pass

class DBClient():
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_connection = None
        self.db_cursor = None

    def connect(self):
        try:
            self.db_connection = sqlite3.connect(self.db_name)
        except sqlite3.OperationalError as e:
            #logging.exception(e)
            raise SQLiteDBConnectException(str(e))

        return self.db_connection

    def cursor(self):
        self.db_cursor = self.db_connection.cursor()
        return self.db_cursor

    def execute(self, sql_executable):
        try:
            self.db_cursor.execute(sql_executable)
        except sqlite3.OperationalError as e:
            #logging.exception(e)
            raise SQLiteDBExecuteException(str(e))

    def commit(self):
        self.db_connection.commit()

    def close(self):
        self.db_connection.close()

db_name = 'test.db'

db = DBClient(db_name)

try:
    db.connect()
except SQLiteDBConnectException as e:
    logging.exception(e)
    print(f'failed to initialize the db connection: {e}', file=sys.stderr)
    sys.exit(2)

db.cursor()

try:
    db.execute("CREATE TABLE snoopy (name TEXT, color TEXT, address TEXT)")
except SQLiteDBExecuteException as e:
    logging.exception(e)
    print(f'failed to create table: {e}', file=sys.stderr)
    sys.exit(2)

try:
    db.execute("INSERT INTO snoopy VALUES ('mydog', 'brown', 'CA')")
except SQLiteDBExecuteException as e:
    logging.exception(e)
    print(f'failed to run sql executable: {e}', file=sys.stderr)

db.commit()
db.close()
