"""
Model for user management
"""

import sqlite3
from hashlib import md5

class Users:
    def __init__(self, connection):
        self.db = connection
        self.cursor = self.db.cursor()

    def user_exists(self, username):
        return not self.cursor.execute(
            "select username from users where username is ?",
            (username,)
        ).fetchone() is None

    def match_password(self, username, password):
        if self.user_exists(username):
            _db_password = self.cursor.execute(
                "select password from users where username is ?",
                (username,)
            ).fetchone()[0]
            return self.encrypt(password) == _db_password
        else:
            return False

    def encrypt(self, password):
        _hex = md5()
        _hex.update(password.encode("utf-8"))
        return _hex.hexdigest()

    def new_user(self, username, password):
        if not self.user_exists(username):
            self.cursor.execute(
                "insert into users ('username', 'password') values (?, ?)",
                (username, self.encrypt(password))
            )
            self.db.commit()
            return True
        else:
            return False

    def delete_user(self, username):
        if self.user_exists(username):
            self.cursor.execute(
                "delete from users where username is ?",
                (username,)
            )
            self.db.commit()
            return True
        else:
            return False

    def list_users(self):
        return [x[0] for x in self.cursor.execute(
            "select username from users"
        ).fetchall()]