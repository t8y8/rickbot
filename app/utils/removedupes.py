#!/usr/bin/python3

import sqlite3

found = []
dupes = []

conn = sqlite3.connect('../rick.db')
cur = conn.cursor()

current_tuples = cur.execute('''SELECT id, saying FROM sayings''').fetchall()

for tup in current_tuples:
    text = "".join([c.lower() for c in tup[1] if c.isalnum()])
    if hash(text) in found:
        dupes.append(tup[0])
    else:
        found.append(hash(text))

print(dupes)

query = 'DELETE FROM sayings WHERE id IN (%s)' % ','.join('?' for i in dupes)

cur.execute(query, dupes)

conn.commit()
conn.close()
