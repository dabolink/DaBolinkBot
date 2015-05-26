import datetime
import Database

class User:
    def __repr__(self):
        return "(" + self.name + ", " + str(self.join_time) + ", " + str(self.admin) + ")"
    def __init__(self, user, join_time, admin=False):
        self.name = user
        self.join_time = join_time
        self.admin = admin
    def __contains__(self, items):
        for item in items:
            if item.name == self.name:
                return True
        return False