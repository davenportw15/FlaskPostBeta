"""
Model for managing user posts
"""

import sqlite3
from datetime import datetime

class Posts(object):
    def __init__(self, connection):
        self.db = connection
        self.cursor = self.db.cursor()

    def post_exists(self, id):
        return not self.cursor.execute(
            "select id from posts where id is ?",
            (id,)
        ).fetchone() is None

    def format_post_data(self, post_data, format_date=True):
            formatted_post = {}
            formatted_post["id"] = post_data[0]
            formatted_post["username"] = post_data[1]
            formatted_post["comment"] = post_data[2]
            if format_date:
                formatted_post["date"] = self.format_date(datetime.strptime(post_data[3], "%Y-%m-%d %H:%M:%S.%f"))
            else:
                formatted_post["date"] = datetime.strptime(post_data[3], "%Y-%m-%d %H:%M:%S.%f")
            return formatted_post

    def format_date(self, date):
        month_names = {
            1:"January",
            2:"February",
            3:"March",
            4:"April",
            5:"May",
            6:"June",
            7:"July",
            8:"August",
            9:"September",
            10:"October",
            11:"November",
            12:"December"
        }

        return "%s %d, %d" % (month_names[date.month], date.day, date.year)

    def get_post_by_id(self, id, format_date=True):
        if self.post_exists(id):
            post_data = self.cursor.execute(
                "select * from posts where id is ?",
                (id,)
            ).fetchone()

            return self.format_post_data(post_data, format_date=format_date)
        else:
            return False

    def list_posts(self):
        posts = self.cursor.execute(
            "select * from posts"
        ).fetchall()

        return list(map(self.format_post_data, posts))

    def list_posts_by_username(self, username):
        posts = self.cursor.execute(
            "select * from posts where username is ? order by id asc",
            (username,)
        ).fetchall()

        return list(map(self.format_post_data, posts))

    def new_post(self, username, comment):
        if username and comment:
            self.cursor.execute(
                "insert into posts ('username','comment','date') values (?,?,?)",
                (username, comment, datetime.now())
            )
            self.db.commit()
            return True
        else:
            return False


    def delete_post_by_id(self, id):
        if self.post_exists(id):
            self.cursor.execute(
                "delete from posts where id is ?",
                (id,)
            )
            self.db.commit()
            return True
        else:
            return False