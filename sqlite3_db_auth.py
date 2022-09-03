#!/usr/bin/env python3

import os
import sqlite3


def authorizer_func(action, arg1, arg2, sql_location, trigger):
    response = sqlite3.SQLITE_OK
    print(action, arg1, arg2, sql_location, trigger)
    if action == sqlite3.SQLITE_SELECT:
        response = sqlite3.SQLITE_OK
    elif action == sqlite3.SQLITE_READ:
        response = sqlite3.SQLITE_OK
    else:
        response = sqlite3.SQLITE_DENY

    return response


if __name__ == "__main__":
    if os.path.exists("test.db"):
        os.unlink("test.db")

    with sqlite3.connect("test.db", uri=True) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE snoopy (name TEXT, color TEXT, address TEXT)")
        cursor.execute("INSERT INTO snoopy VALUES ('mydog', 'brown', 'CA')")

    print("RW mode + SELECT authorizer")
    with sqlite3.connect(f"file:test.db?mode=rw", uri=True) as conn:
        conn.set_authorizer(authorizer_func)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM snoopy")
        print(cursor.fetchall())
        try:
            cursor.execute("DROP TABLE snoopy")
        except Exception as e:
            if isinstance(e, sqlite3.DatabaseError):
                print(str(e))

    print()

    print("RO mode + SELECT authorizer")
    with sqlite3.connect(f"file:test.db?mode=ro", uri=True) as conn:
        conn.set_authorizer(authorizer_func)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM snoopy")
        print(cursor.fetchall())
        try:
            cursor.execute("DROP TABLE snoopy")
        except Exception as e:
            if isinstance(e, sqlite3.DatabaseError):
                print(str(e))

    print()

    print("RO mode")
    with sqlite3.connect(f"file:test.db?mode=ro", uri=True) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM snoopy")
        print(cursor.fetchall())
        try:
            cursor.execute("DROP TABLE snoopy")
        except Exception as e:
            if isinstance(e, sqlite3.OperationalError):
                print(str(e))
