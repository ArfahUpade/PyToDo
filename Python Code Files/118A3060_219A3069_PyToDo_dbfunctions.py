import sqlite3

conn = sqlite3.connect('PyToDo.db')
#q1 = "DROP Table todo"
#conn.execute(q1)
#q = "CREATE TABLE todo (id INTEGER PRIMARY KEY, task TEXT NOT NULL, dateoftask TEXT, timeoftask TEXT);"
#conn.execute(q)


def show():
    query = "SELECT * FROM todo;"
    return conn.execute(query)

def insertdata(task, timeoftask, dateoftask):
    query = "INSERT INTO todo(task, timeoftask, dateoftask) VALUES(?,?,?);"
    conn.execute(query, (task, timeoftask, dateoftask))
    conn.commit()

def datetime(task):
    query = "SELECT dateoftask, timeoftask FROM todo where task=?;"
    conn.execute(query, (task,))
    for rows in conn.execute(query,(task,)):
        print(rows)


def deletebyid(taskid):
    query = "DELETE FROM todo WHERE id =?;"
    conn.execute(query, (taskid,))
    conn.commit()

def deletebytask(taskval):
    query = "DELETE FROM todo WHERE task =?;"
    conn.execute(query, (taskval,))
    conn.commit()


def updatedata(task, newtime, newdate):
    query = "UPDATE todo SET timeoftask = ?, dateoftask = ? WHERE task = ?;"
    conn.execute(query, (newtime, newdate, task))
    conn.commit()


'''
updatedata(2, "AM IV - Gauss Lemma Exercise", "07:50:00", "2020-04-26", "-", "-")
'''
query = 'SELECT * FROM todo;'
for rows in conn.execute(query):
    print(rows)

print('Database Connected')
'''
conn.close()
'''
