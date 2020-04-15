#!/usr/bin/env python3
import sqlite3
from time import time
from uuid import uuid1

from flask import Flask, jsonify, abort, request, make_response, g
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import properties
from database import Database

APP = Flask(__name__)
AUTH = HTTPBasicAuth()
DATABASE = Database()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d


def conn_get():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(properties.db_name)
        conn.row_factory = dict_factory

    return conn


@APP.teardown_appcontext
def conn_close(_):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()


@AUTH.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Forbidden'}), 403)


@APP.errorhandler(400)
def not_found(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@APP.errorhandler(409)
def not_found(_):
    return make_response(jsonify({'error': 'Conflict'}), 409)


@APP.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not Found'}), 404)


@APP.errorhandler(500)
def not_found(_):
    return make_response(jsonify({'error': 'Internal Error'}), 500)


@AUTH.verify_password
def verify_password(username, password):
    conn = conn_get()
    user = DATABASE.get_user(conn, username)
    if user == None:
        return False

    return check_password_hash(user['password'], password)


@APP.route('/api/v1/auth', methods=['GET'])
@AUTH.login_required
def authenticate():
    return ""


@APP.route('/api/v1/auth', methods=['POST'])
def register():
    if not request.json \
            or not 'username' in request.json or len(request.json['username']) == 0 \
            or not 'password' in request.json or len(request.json['password']) == 0:
        abort(400)

    conn = conn_get()
    user = DATABASE.get_user(conn, request.json['username'])
    if user is not None:
        abort(409)

    user = {
        'username': request.json['username'],
        'password': generate_password_hash(request.json['password']),
    }
    DATABASE.add_user(conn, user)

    return "", 201


@APP.route('/api/v1/session', methods=['POST'])
@AUTH.login_required
def create_session():
    if not request.json \
            or not 'payload' in request.json:
        abort(400)

    conn = conn_get()
    session = {
        'uuid': str(uuid1()),
        'users': [AUTH.username()],
        'payload': request.json['payload'],
        'state': 'New',
        'ts': int(time()),
    }
    DATABASE.add_session(conn, session)

    return jsonify(session), 201


@APP.route('/api/v1/session/<string:uuid>', methods=['GET'])
@AUTH.login_required
def get_session(uuid):
    conn = conn_get()
    session = DATABASE.get_session(conn, uuid)
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

        DATABASE.update_session(conn, session)

    return jsonify(session)


if __name__ == '__main__':
    APP.run(debug=False)
