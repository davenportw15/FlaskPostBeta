import sqlite3

class Admin:
    def __init__(self, connection):
        self.db = connection
        self.cursor = self.db.cursor()

    def admin_exists(self, username):
        return not self.cursor.execute(
            "select username from admin where username is ?",
            (username,)).fetchone() is None

    def new_admin(self, username):
        if not self.admin_exists(username):
            self.cursor.execute(
                "insert into admin ('username') values (?)",
                (username,)
            )
            self.db.commit()
        else:
            return False

    def delete_admin(self, username):
        if self.admin_exists(username):
            self.cursor.execute(
                "delete from admin where username is ?",
                (username,)
            )
            self.db.commit()
        else:
            return False