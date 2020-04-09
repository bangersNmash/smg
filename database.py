"""
database.py -- db interface
=================================
Used in server.py
"""

import json
import sql


def init(conn):
    """"Initializes DB state"""

    cursor = conn.cursor()
    cursor.execute(sql.CREATE_USERS)
    cursor.execute(sql.CREATE_SESSIONS)
    conn.commit()
    conn.close()


def get_user(conn, username):
    """get user by username"""

    cursor = conn.cursor()
    cursor.execute(sql.SELECT_USER, (username,))
    return cursor.fetchone()


def add_user(conn, user):
    """add new user"""

    cursor = conn.cursor()
    cursor.execute(sql.INSERT_USER, (user['username'], user['password']))
    conn.commit()


def get_session(conn, uuid):
    """get session by uuid"""

    cursor = conn.cursor()
    cursor.execute(sql.SELECT_SESSION, (uuid,))
    session = cursor.fetchone()
    if session is None:
        return None

    session['users'] = list(json.loads(session['users']))
    session['payload'] = json.loads(session['payload'])
    return session


def add_session(conn, session):
    """add new session"""

    cursor = conn.cursor()
    cursor.execute(sql.INSERT_SESSION, (
        session['uuid'],
        json.dumps(session['users']),
        json.dumps(session['payload']),
        session['state'],
        session['ts']
    ))
    conn.commit()


def update_session(conn, session):
    """update existing session"""

    cursor = conn.cursor()
    cursor.execute(sql.UPDATE_SESSION, (
        json.dumps(session['users']),
        json.dumps(session['payload']),
        session['state'],
        session['ts'],
        session['uuid']
    ))
    conn.commit()
