import sqlite3
from activitybot.queries import *
from activitybot.config import ADMINS


class Database:
    def __init__(self, path) -> None:
        self.path = path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        self.connection = sqlite3.connect(self.path, check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def execute_sql(self, sql):
        self.check_if_connected()
        res = self.cursor.execute(sql)
        result = res.fetchall()
        self.connection.commit()
        return result
    
    def execute_list(self, sql_list):
        results = []
        self.check_if_connected()
        for sql in sql_list:
            res = self.cursor.execute(sql)
            results.append(res.fetchall())
            self.connection.commit()
        return results
    
    def user_exists(self, user_id):
        return len(self.execute_sql(get_user(telegram_id=user_id))) > 0
    
    @property
    def connected(self):
        return not self.cursor is None
    
    def check_if_connected(self):
        if not self.connected:
            raise ConnectionError("Database is not connected")
        
    def is_admin(self, telegram_id: str):
        return str(telegram_id) in ADMINS
