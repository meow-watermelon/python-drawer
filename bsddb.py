#!/usr/bin/env python3

import bsddb3
import os

if __name__ == '__main__':
    db_name = 'kv.db'

    if os.path.exists(db_name):
        os.remove(db_name)

    data = {
        'apple': 'CA',
        'pinterest': 'CA',
        'microsoft': 'WA',
        'amazon': 'WA',
        'redhat': 'NC',
    }

    # set up db
    db = bsddb3.db.DB()
    db.open('kv.db', bsddb3.db.DB_BTREE, bsddb3.db.DB_CREATE)

    for k,v in data.items():
        db.put(k.encode(), v.encode())

    db.sync()
    db.close()

    # retrieve items
    db = bsddb3.db.DB()
    db.open('kv.db', bsddb3.db.DB_BTREE, bsddb3.db.DB_RDONLY)

    for k in db.keys():
        v = db.get(k)
        print('%s => %s' %(k.decode('ascii'), v.decode('ascii')))

    db.close()
