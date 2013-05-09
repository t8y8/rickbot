#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect('../rick.db')
cur = conn.cursor()

results = cur.execute('''SELECT id, saying FROM sayings''').fetchall()

count = 0

for i in results:
    print("{} | {}".format(i[0], i[1]
                   .encode('latin1', 'replace').decode('utf8')))
    count += 1

print(count)
conn.close()
