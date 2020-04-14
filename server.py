#!/usr/bin/env python3
import sqlite3
from flask import Flask, jsonify, abort, request, make_response, g
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database
from uuid import uuid1
from time import time

app = Flask(__name__)
auth = HTTPBasicAuth()
database = Database()




def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d


def conn_get():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect("mydatabase.db")
        conn.row_factory = dict_factory

    return conn


@app.teardown_appcontext
def conn_close(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()




@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Forbidden'}), 403)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(409)
def not_found(error):
    return make_response(jsonify({'error': 'Conflict'}), 409)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Internal Error'}), 500)




@auth.verify_password
def verify_password(username, password):
    conn = conn_get()
    user = database.get_user(conn, username)
    if user == None:
        return False

    return check_password_hash(user['password'], password)


@app.route('/api/v1/auth', methods=['GET'])
@auth.login_required
def authenticate():
    return ""


@app.route('/api/v1/auth', methods=['POST'])
def register():
    if not request.json \
        or not 'username' in request.json or len(request.json['username']) == 0 \
        or not 'password' in request.json or len(request.json['password']) == 0:
            abort(400)

    conn = conn_get()
    user = database.get_user(conn, request.json['username'])
    if user != None:
        abort(409)

    user = {
        'username': request.json['username'],
        'password': generate_password_hash(request.json['password']),
    }
    database.add_user(conn, user)

    return "", 201




@app.route('/api/v1/session', methods=['POST'])
@auth.login_required
def create_session():
    if not request.json \
        or not 'payload' in request.json:
            abort(400)

    conn = conn_get()
    session = {
        'uuid': str(uuid1()),
        'users': [auth.username()],
        'payload': request.json['payload'],
        'state': 'New',
        'ts': int(time()),
    }
    database.add_session(conn, session)

    return jsonify(session), 201


@app.route('/api/v1/session/<string:uuid>', methods=['GET'])
@auth.login_required
def get_session(uuid):
    conn = conn_get()
    session = database.get_session(conn, uuid)
    if session == None:
        abort(404)

    if session['state'] in ['Started', 'Finished']:
        if auth.username() not in session['users']:
            abort(404)

        return jsonify(session)

    if auth.username() not in session['users']:
        session['users'].append(auth.username())
        session['ts'] = int(time())

        if 'players' in session['payload']:
            if session['payload']['players'] == len(session['users']):
                session['state'] = 'Started'
        elif len(session['users']) == 2:
                session['state'] = 'Started'

        database.update_session(conn, session)

    return jsonify(session)




if __name__ == '__main__':
    app.run(debug=False)
