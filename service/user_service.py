from db import Database

class UserService:
    def __init__(self):
        self.db = Database.get_instance()

    def add_user(self, username, password, role, eid=None):
        return self.db.add_user(username, password, role, eid)

    def get_users(self):
        return self.db.get_users()
    #authentication of user
    def authenticate(self, username, password):
        user = self.db.get_user_by_username(username)
        if user and user.pwd == password:
            return user
        return None