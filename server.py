#!/usr/bin/env python3
"""
server.py -- http api server
========================
Http api server for smg client
Provides auth and game session api
Validates game state
"""

import sqlite3
from time import time
from uuid import uuid1

from flask import Flask, jsonify, abort, request, make_response, g
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import properties
import database

APP = Flask(__name__)
AUTH = HTTPBasicAuth()
database.init(sqlite3.connect(properties.db_name))


def dict_factory(cursor, row):
    """Return DB tuple as dict"""

    ret = {}
    for idx, col in enumerate(cursor.description):
        ret[col[0]] = row[idx]

    return ret


def conn_get():
    """Return DB connection, creates connection if needed"""

    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(properties.db_name)
        conn.row_factory = dict_factory

    return conn


@APP.teardown_appcontext
def conn_close(_):
    """Close DB connection"""

    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()


@AUTH.error_handler
def forbidden():
    """403 status wrapper"""

    return make_response(jsonify({'error': 'Forbidden'}), 403)


@APP.errorhandler(400)
def bad_request(_):
    """400 status wrapper"""

    return make_response(jsonify({'error': 'Bad Request'}), 400)


@APP.errorhandler(409)
def conflict(_):
    """409 status wrapper"""

    return make_response(jsonify({'error': 'Conflict'}), 409)


@APP.errorhandler(404)
def not_found(_):
    """404 status wrapper"""

    return make_response(jsonify({'error': 'Not Found'}), 404)


@APP.errorhandler(500)
def internal(_):
    """500 status wrapper"""
    return make_response(jsonify({'error': 'Internal Error'}), 500)


@AUTH.verify_password
def verify_password(username, password):
    """Validate password"""

    conn = conn_get()
    user = database.get_user(conn, username)
    if user is None:
        return False

    return check_password_hash(user['password'], password)


@APP.route('/api/v1/auth', methods=['GET'])
@AUTH.login_required
def authenticate():
    """
    Api.auth method
    arguments: []
    returns: empty body
    200 -- auth success
    403 -- wrong authorization
    500 -- internal error
    """

    return ""


@APP.route('/api/v1/auth', methods=['POST'])
def register():
    """
    Api.register method
    arguments: [username, password]
    returns: empty body
    201 -- registration success
    400 -- wrong arguments
    409 -- username exists
    500 -- internal error
    """

    if not request.json \
            or not 'username' in request.json or len(request.json['username']) == 0 \
            or not 'password' in request.json or len(request.json['password']) == 0:
        abort(400)

    conn = conn_get()
    user = database.get_user(conn, request.json['username'])
    if user is not None:
        abort(409)

    user = {
        'username': request.json['username'],
        'password': generate_password_hash(request.json['password']),
    }
    database.add_user(conn, user)

    return "", 201


@APP.route('/api/v1/session', methods=['POST'])
@AUTH.login_required
def create_session():
    """
    Api.create_session method
    arguments: [payload]
    returns: [uuid, users, payload, state, ts]
    201 -- session created
    400 -- wrong arguments
    403 -- wrong authorization
    500 -- internal error
    """

    if not request.json or not 'payload' in request.json:
        abort(400)

    conn = conn_get()
    session = {
        'uuid': str(uuid1()),
        'users': [AUTH.username()],
        'payload': request.json['payload'],
        'state': 'New',
        'ts': int(time()),
    }
    database.add_session(conn, session)

    return jsonify(session), 201


@APP.route('/api/v1/session/<string:uuid>', methods=['GET'])
@AUTH.login_required
def get_session(uuid):
    """
    Api.get_session method
    returns: [uuid, users, payload, state, ts]
    200 -- session created
    400 -- wrong arguments
    403 -- wrong authorization
    404 -- session not found
    500 -- internal error
    """

    conn = conn_get()
    session = database.get_session(conn, uuid)
    if session is None:
        abort(404)

    if session['state'] in ['Started', 'Finished']:
        if AUTH.username() not in session['users']:
            abort(404)

        return jsonify(session)

    if AUTH.username() not in session['users']:
        session['users'].append(AUTH.username())
        session['ts'] = int(time())

        if 'players' in session['payload']:
            if session['payload']['players'] == len(session['users']):
                session['state'] = 'Started'
        elif len(session['users']) == properties.default_players:
            session['state'] = 'Started'

        database.update_session(conn, session)

    return jsonify(session)


if __name__ == '__main__':
    APP.run(debug=False)
