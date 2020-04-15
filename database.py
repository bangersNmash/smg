import json
import sqlite3

import properties
import sql


class Database:
    """Database interface"""

    def __init__(self):
        conn = sqlite3.connect(properties.db_name)
        cursor = conn.cursor()
        cursor.execute(sql.CREATE_USERS)
        cursor.execute(sql.CREATE_SESSIONS)
        conn.commit()
        conn.close()

    def get_user(self, conn, username):
        cursor = conn.cursor()
        cursor.execute(sql.SELECT_USER, (username,))
        return cursor.fetchone()

    def add_user(self, conn, user):
        cursor = conn.cursor()
        cursor.execute(sql.INSERT_USER, (user['username'], user['password']))
        conn.commit()

    def get_session(self, conn, uuid):
        cursor = conn.cursor()
        cursor.execute(sql.SELECT_SESSION, (uuid,))
        session = cursor.fetchone()
        if session is None:
            return None

        session['users'] = list(json.loads(session['users']))
        session['payload'] = json.loads(session['payload'])
        return session

    def add_session(self, conn, session):
        cursor = conn.cursor()
        cursor.execute(sql.INSERT_SESSION, (
            session['uuid'],
            json.dumps(session['users']),
            json.dumps(session['payload']),
            session['state'],
            session['ts']
        ))
        conn.commit()

    def update_session(self, conn, session):
        cursor = conn.cursor()
        cursor.execute(sql.UPDATE_SESSION, (
            json.dumps(session['users']),
            json.dumps(session['payload']),
            session['state'],
            session['ts'],
            session['uuid']
        ))
        conn.commit()
