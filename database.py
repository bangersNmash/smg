import sqlite3
import json
import sql
import properties
 
 
"""Database interface"""
class Database:
    def __init__(self):
        conn   = sqlite3.connect(properties.db_name)
        cursor = conn.cursor()
        cursor.execute(sql.create_users)
        cursor.execute(sql.create_sessions)
        conn.commit()
        conn.close()


    def get_user(self, conn, username):
        cursor = conn.cursor()
        cursor.execute(sql.select_user, (username,))
        return cursor.fetchone()


    def add_user(self, conn, user):
        cursor = conn.cursor()
        cursor.execute(sql.insert_user, (user['username'], user['password']))
        conn.commit()


    def get_session(self, conn, uuid):
        cursor = conn.cursor()
        cursor.execute(sql.get_session, (uuid,))
        session = cursor.fetchone()
        session['users']   = list(json.loads(session['users']))
        session['payload'] = json.loads(session['payload'])
        return session


    def add_session(self, conn, session):
        cursor = conn.cursor()
        cursor.execute(sql.insert_session, (
                           session['uuid'],
                           json.dumps(session['users']),
                           json.dumps(session['payload']),
                           session['state'],
                           session['ts']
        ))
        conn.commit()


    def update_session(self, conn, session):
        cursor = conn.cursor()
        cursor.execute(sql.update_session, (
                           json.dumps(session['users']),
                           json.dumps(session['payload']),
                           session['state'],
                           session['ts'],
                           session['uuid']
        ))
        conn.commit()
