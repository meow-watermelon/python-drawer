#!/usr/bin/env python3

import logging
import os
import sqlite3
import sys


class SQLiteDBConnectException(Exception):
    pass


class SQLiteDBExecuteException(Exception):
    pass


class DBClient:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_connection = None
        self.db_cursor = None

    def connect(self):
        try:
            self.db_connection = sqlite3.connect(self.db_name)
        except sqlite3.OperationalError as e:
            raise SQLiteDBConnectException(str(e))

    def cursor(self):
        self.db_cursor = self.db_connection.cursor()

    def execute(self, sql_executable, parameters=None):
        if parameters is None:
            parameters = ()

        try:
            self.db_cursor.execute(sql_executable, parameters)
        except sqlite3.OperationalError as e:
            raise SQLiteDBExecuteException(str(e))

        return self.db_cursor

    def commit(self):
        self.db_connection.commit()

    def close(self):
        self.db_connection.close()


dogs = {
    "alpha": {
        "color": "black",
        "address": "USA",
    },
    "beta": {
        "color": "red",
        "address": "CANADA",
    },
    "gamma": {
        "color": "brown",
        "address": "UK",
    },
}

db_name = "test.db"

if os.path.exists(db_name):
    os.remove(db_name)

db = DBClient(db_name)

try:
    db.connect()
except SQLiteDBConnectException as e:
    logging.exception(e)
    print(f"failed to initialize the db connection: {e}", file=sys.stderr)
    sys.exit(2)

db.cursor()

try:
    db.execute("CREATE TABLE snoopy (name TEXT, color TEXT, address TEXT)")
except SQLiteDBExecuteException as e:
    logging.exception(e)
    print(f"failed to create table: {e}", file=sys.stderr)
    sys.exit(2)

for name in dogs.keys():
    color = dogs.get(name).get("color")
    address = dogs.get(name).get("address")

    try:
        db.execute("INSERT INTO snoopy VALUES (?, ?, ?)", (name, color, address))
    except SQLiteDBExecuteException as e:
        logging.exception(e)
        print(f"failed to run sql executable: {e}", file=sys.stderr)

db.commit()

for row in db.execute("SELECT * FROM snoopy"):
    print(row)

db.close()
