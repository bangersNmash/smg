class Database:
    """Database interface"""
    data = {}

    def __init__(self, data):
        self.data = data


    def get_user(self, username):
        user = list(filter(lambda u: u['username'] == username, self.data['users']))
        if len(user) == 0:
            return None

        return user[0]


    def add_user(self, user):
        self.data['users'].append(user)


    def get_session(self, uuid):
        session = list(filter(lambda s: s['uuid'] == uuid, self.data['sessions']))
        if len(session) == 0:
            return None

        return session[0]


    def add_session(self, session):
        self.data['sessions'].append(session)


    def update_session(self, session):
        return
