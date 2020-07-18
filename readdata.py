import sqlite3
arr = []
class fillArr:
    def __init__(self):
        try:
            con = sqlite3.connect("database.db")
            self.read_table(con)
        except sqlite3.Error as e:
            print(e)

    def read_table(self,con):
        cur = con.cursor()
        cur.execute("SELECT * FROM List")

        rows = cur.fetchall()

        for row in rows:
            arr.append(row)
    return arr

x = fillArr()
print(fillArr.read_table)
print(x)