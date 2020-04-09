#!/usr/bin/env python3
from flask import Flask, jsonify, abort, request, make_response
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

database = {
    'users': [
        {'login': 'max', 'password': '123'}
    ],
    'tasks': [
        {'id': 1, 'title': 'first'}, {'id': 2, 'title': 'second'}
    ]
}


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Forbidden'}), 403)

@auth.get_password
def get_password(login):
    user = list(filter(lambda u: u['login'] == login, database['users']))
    if len(user) == 0:
        return None
    return user[0]['password']


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Internal Error'}), 500)


@app.route('/api/v1/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': database['tasks']})

@app.route('/api/v1/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, database['tasks']))
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/api/v1/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': database['tasks'][-1]['id'] + 1,
        'title': request.json['title'],
    }
    database['tasks'].append(task)
    return jsonify({'task': task}), 201

@app.route('/api/v1/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, database['tasks']))
    if len(task) == 0 or not request.json: 
        abort(404)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    return jsonify({'task': task[0]})

@app.route('/api/v1/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, database['tasks']))
    if len(task) == 0:
        abort(404)
    database['tasks'].remove(task[0])
    return jsonify({'task': task[0]})

if __name__ == '__main__':
    app.run(debug=False)
