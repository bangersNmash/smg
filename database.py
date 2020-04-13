import sqlite3
import json
 
 
class Database:
    """Database interface"""
    data = ""
    def __init__(self):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                           username VARCHAR PRIMARY KEY,
                           password VARCHAR NOT NULL)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS sessions(
                           uuid VARCHAR PRIMARY KEY,
                           users VARCHAR NOT NULL,
                           payload VARCHAR NOT NULL,
                           state VARCHAR NOT NULL,
                           ts INT NOT NULL)""")
        conn.commit()
        conn.close()


    def get_user(self, conn, username):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return cursor.fetchone()


    def add_user(self, conn, user):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?)",
                           (user['username'], user['password']))
        conn.commit()


    def get_session(self, conn, uuid):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE uuid=?", (uuid,))
        session = cursor.fetchone()
        session['users'] = list(json.loads(session['users']))
        session['payload'] = json.loads(session['payload'])
        return session


    def add_session(self, conn, session):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sessions VALUES (?,?,?,?,?)",
                           (session['uuid'],
                           json.dumps(session['users']),
                           json.dumps(session['payload']),
                           session['state'],
                           session['ts']))
        conn.commit()


    def update_session(self, conn, session):
        cursor = conn.cursor()
        cursor.execute("UPDATE sessions SET users=?, payload=?, state=?, ts=? WHERE uuid=?",
                           (json.dumps(session['users']),
                           json.dumps(session['payload']),
                           session['state'],
                           session['ts'],
                           session['uuid']))
        conn.commit()
