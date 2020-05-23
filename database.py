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
    cursor.execute(sql.CREATE_ROUNDS)
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
        session['players'],
        json.dumps(session['payload']),
        session['state'],
        session['round'],
        session['ts']
    ))


def update_session(conn, session):
    """update existing session"""

    cursor = conn.cursor()
    cursor.execute(sql.UPDATE_SESSION, (
        json.dumps(session['users']),
        session['players'],
        json.dumps(session['payload']),
        session['state'],
        session['round'],
        session['ts'],
        session['uuid']
    ))


def get_round(conn, uuid, rnd):
    """get session_round by uuid and round"""

    cursor = conn.cursor()
    cursor.execute(sql.SELECT_ROUND, (uuid, rnd))
    session_round = cursor.fetchone()
    if session_round is None:
        return None

    session_round['user_moves'] = json.loads(session_round['user_moves'])
    return session_round


def add_round(conn, session_round):
    """add new session_round"""

    cursor = conn.cursor()
    cursor.execute(sql.INSERT_ROUND, (
        session_round['uuid'],
        session_round['round'],
        json.dumps(session_round['user_moves']),
    ))


def update_round(conn, session_round):
    """update existing session_round"""

    cursor = conn.cursor()
    cursor.execute(sql.UPDATE_ROUND, (
        json.dumps(session_round['user_moves']),
        session_round['uuid'],
        session_round['round'],
    ))
