## basic/imp queries im sqlite3 from python

## first connect your db
```
import sqlite3
con = sqlite3.connect(path)
cur = con.cursor()

```

## pass your queries

### select last row from col

```
r = cur.execute('SELECT * FROM table ORDER BY column DESC LIMIT 1')
r.fetchall()
con.close()
```

### select all rows where columns = 1


```
cur.execute("select * from table where x=:year", {"year": 1})
print(cur.fetchall())
```

### select n last rows where columns = 1

```

SELECT * FROM table ORDER BY id DESC LIMIT 50

cur.execute("select * from table where x=:year LIMIT 4", {"year": 1})
for row in cur:
    print(row)
con.close()

```
