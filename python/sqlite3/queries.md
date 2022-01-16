## basic/imp queries im sqlite3 from python

## first connect your db
```
import sqlite3
con = sqlite3.connect(path)
cur = con.cursor()

```

# Never do this -- insecure!
symbol = 'RHAT'
cur.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)


```
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("create table lang (name, first_appeared)")

# This is the qmark style:
cur.execute("insert into lang values (?, ?)", ("C", 1972))

# The qmark style used with executemany():
lang_list = [
    ("Fortran", 1957),
    ("Python", 1991),
    ("Go", 2009),
]
cur.executemany("insert into lang values (?, ?)", lang_list)

# And this is the named style:
cur.execute("select * from lang where first_appeared=:year", {"year": 1972})
print(cur.fetchall())

con.close()
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
