#!/usr/bin/env python3
from flask import Flask, jsonify, abort, request, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database
from uuid import uuid1
from time import time

app = Flask(__name__)
auth = HTTPBasicAuth()
database = Database({
    'users': [
        {'username': 'max1', 'password': generate_password_hash('123')},
        {'username': 'max2', 'password': generate_password_hash('123')}
    ],
    'sessions': []
})



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
    user = database.get_user(username)
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
        or not 'username' in request.json \
        or not 'password' in request.json:
            abort(400)

    user = database.get_user(request.json['username'])
    if user != None:
        abort(409)

    user = {
        'username': request.json['username'],
        'password': generate_password_hash(request.json['password']),
    }
    database.add_user(user)

    return "", 201




@app.route('/api/v1/session', methods=['POST'])
@auth.login_required
def create_session():
    if not request.json \
        or not 'data' in request.json:
            abort(400)

    session = {
        'uuid': str(uuid1()),
        'data': request.json['data'],
        'creator': auth.username(),
        'started': False,
        'ts': int(time()),
    }
    database.add_session(session)

    return jsonify(session), 201


@app.route('/api/v1/session/<string:uuid>', methods=['GET'])
@auth.login_required
def get_session(uuid):
    session = database.get_session(uuid)
    if session == None:
        abort(404)

    if session['started']:
        if auth.username() not in [session['creator'], session['opponent']]:
            abort(404)

        return jsonify(session)

    if session['creator'] != auth.username():
        session['started'] = True
        session['opponent'] = auth.username()
        session['ts'] = int(time())
        database.update_session(session)

    return jsonify(session)




if __name__ == '__main__':
    app.run(debug=False)
