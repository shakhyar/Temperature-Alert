import sqlite3
from config import DB_PATH

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()




class Users:
    # simple database managent script here
    # valriable and function names are clear enough to describe
    # their uses. Refer to Docs for more
    def __init__(self):
        self.create_table(True)

    def create_table(self, true):
        self.true = true
        if self.true:
            c.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, maxt INT, mint INT, lat REAL, ln REAL, email TEXT)")
            conn.commit()
        else:
            pass

    def data_entry(self, name, maxt, mint, ln, lat, email):

        c.execute("INSERT INTO users(name, maxt, mint, lat, ln, email) VALUES (?,?,?,?,?,?)",
            (name, maxt, mint, ln, lat, email))
        conn.commit()


    def read(self):
        c.execute("SELECT * FROM users")
        self.data = []
        for row in c.fetchall():
            self.data.append(row)

        return self.data
    

    def get_coordinates(self):
        c.execute("SELECT lat, ln FROM users")
        self.cor = []
        for row in c.fetchall():
            self.cor.append(row)

        return self.cor

    def get_ranges(self):
        c.execute("SELECT maxt, mint FROM users")
        self.cor = []
        for row in c.fetchall():
            self.cor.append(row)
        return self.cor

    def get_emails(self):
        c.execute("SELECT email, name FROM users")
        self.cor = []
        for row in c.fetchall():
            self.cor.append(row)
        return self.cor


    def delete(self, email):
        self.email = email
        c.execute("DELETE FROM users WHERE email = ?", (self.email,))
        conn.commit()
        print("cleared", self.email)