import requests
import properties

def health_check():
    res = requests.get(properties.server_url + "/health_check")
    return res.status_code, res.json()


"""
register({"username":"maxx", "password":"123"})
201 - created
400 - wrong request
409 - username already exists
500 - internal error
"""
def register(user):
    res = requests.post(
        properties.server_url + "/auth",
        json = user
    )
    return res.status_code


"""
auth({"username":"maxx", "password":"123"})
200 - success
403 - wrong auth
500 - internal error
"""
def auth(user):
    res = requests.get(
        properties.server_url + "/auth",
        auth = (user['username'], user['password'])
    )
    return res.status_code


"""
create_session({"username":"maxx", "password":"123"}, any_dict)
returns: [uuid, users, players, payload, state, round, ts]
201 - created
400 - bad request
403 - wrong auth
500 - internal error
"""
def create_session(user, payload):
    res = requests.post(
        properties.server_url + "/session",
        json = {"payload":payload},
        auth = (user['username'], user['password'])
    )
    return res.status_code, res.json()


"""
get_session({"username":"maxx", "password":"123"}, {"uuid":"session_uuid"})
returns: [uuid, users, players, payload, state, round, ts]
200 - success
403 - wrong auth
404 - session not found
500 - internal error
"""
def get_session(user, session):
    res = requests.get(
        properties.server_url + "/session/" + session['uuid'],
        auth = (user['username'], user['password'])
    )
    return res.status_code, res.json()


"""
make_move({"username":"maxx", "password":"123"}, any_dict, {"uuid":"session_uuid", "round":1})
200 - move accepted
400 - bad request
403 - wrong auth
404 - session not found
406 - move can't be accepted
500 - internal error
"""
def make_move(user, payload, session):
    res = requests.put(
        properties.server_url + "/session/" + session['uuid'],
        json = {"payload":payload, "round":session['round'], "hash":"not_implemented"},
        auth = (user['username'], user['password'])
    )
    return res.status_code


"""
get_moves({"username":"maxx", "password":"123"}, {"uuid":"session_uuid", "round":1})
returns: [uuid, round, move, user_moves, ts]
200 - success
403 - wrong auth
404 - session not found
406 - wrong round
500 - internal error
"""
def get_moves(user, session):
    res = requests.get(
        properties.server_url + "/session/" + session['uuid'] + "/" + str(session['round']),
        auth = (user['username'], user['password'])
    )
    return res.status_code, res.json()
