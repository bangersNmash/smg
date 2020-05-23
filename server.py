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

import database
import properties

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


@APP.errorhandler(406)
def not_acceptable(_):
    """406 status wrapper"""

    return make_response(jsonify({'error': 'Not Acceptable'}), 406)


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
    conn.commit()

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

    players = properties.default_players
    if 'players' in request.json['payload'] and isinstance(request.json['payload'], int):
        players = request.json['payload']

    conn = conn_get()
    session = {
        'uuid': str(uuid1()),
        'users': [AUTH.username()],
        'players': players,
        'payload': request.json['payload'],
        'state': 'New',
        'round': 0,
        'ts': int(time()),
    }
    database.add_session(conn, session)
    conn.commit()

    return jsonify(session), 201


@APP.route('/api/v1/health_check', methods=['GET'])
def health_check():
    """
    Api.health_check method
    returns status "ok" or fails
    """
    return jsonify({"status": "ok"})


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

        if len(session['users']) == session['players']:
            session['state'] = 'Started'
            session['round'] = 1
            database.add_round(conn, {
                'uuid': uuid,
                'round': 1,
                'user_moves': {},
            })

        database.update_session(conn, session)
        conn.commit()

    return jsonify(session)


@APP.route('/api/v1/session/<string:uuid>', methods=['PUT'])
@AUTH.login_required
def make_move(uuid):
    """
    Api.make_move method
    arguments: [hash, round, payload]
    returns: empty body
    200 -- move accepted
    400 -- wrong arguments
    403 -- wrong authorization
    404 -- session not found
    406 -- session is not active
    406 -- wrong round
    406 -- round already expired
    500 -- internal error
    """

    if not request.json or \
            not 'hash' in request.json or \
            not 'round' in request.json or \
            not 'payload' in request.json:
        abort(400)

    conn = conn_get()
    session = database.get_session(conn, uuid)
    if session is None or AUTH.username() not in session['users']:
        abort(404)

    if session['state'] != 'Started':
        abort(406)

    if request.json['round'] != session['round']:
        abort(406)

    session_round = database.get_round(conn, uuid, session['round'])
    if session_round is None:
        abort(500)

    if session['ts'] + properties.round_duration < int(time()):
        session['round'] = session['round'] + 1
        session['ts'] = int(time())
        database.update_session(conn, session)
        database.add_round(conn, {
            'uuid': uuid,
            'round': session['round'],
            'user_moves': {},
        })
        conn.commit()
        abort(406)

    if AUTH.username() not in session_round['user_moves']:
        session_round['user_moves'][AUTH.username()] = request.json['payload']
        database.update_round(conn, session_round)
        if len(session_round['user_moves']) == session['players']:
            session['round'] = session['round'] + 1
            session['ts'] = int(time())
            database.update_session(conn, session)
            database.add_round(conn, {
                'uuid': uuid,
                'round': session['round'],
                'user_moves': {},
            })
        conn.commit()

    return "", 200


@APP.route('/api/v1/session/<string:uuid>/<int:rnd>', methods=['GET'])
@AUTH.login_required
def get_moves(uuid, rnd):
    """
    Api.get_moves method
    returns: [uuid, round, move, user_moves, ts]
    200 -- moves returned
    403 -- wrong authorization
    404 -- session not found
    406 -- session is not active
    406 -- wrong round
    500 -- internal error
    """

    conn = conn_get()
    session = database.get_session(conn, uuid)
    if session is None or AUTH.username() not in session['users']:
        abort(404)

    if session['state'] != 'Started':
        abort(406)

    if rnd > session['round'] and rnd > 0:
        abort(406)

    session_round = database.get_round(conn, uuid, rnd)
    if session_round is None:
        abort(500)

    move = False
    if session['ts'] + properties.round_duration < int(time()):
        session['round'] = session['round'] + 1
        session['ts'] = int(time())
        database.update_session(conn, session)
        database.add_round(conn, {
            'uuid': uuid,
            'round': session['round'],
            'user_moves': {},
        })
        conn.commit()
        move = True

    if len(session_round['user_moves']) == session['players']:
        move = True

    session_round['ts'] = session['ts']
    session_round['move'] = move

    return jsonify(session_round)


if __name__ == '__main__':
    APP.run(debug=False)
