import pymysql.cursors
from flask import g


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host="sae206.mysql.pythonanywhere-services.com",
            user="sae206",
            password="saeMySQL",
            database="sae206$saebdd",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return db
