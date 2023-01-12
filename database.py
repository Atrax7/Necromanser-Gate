import sqlite3
import sys


class DataBase:
    def __init__(self):
        self.nickname = None
        try:
            self.con = sqlite3.connect("data/database.db")
            self.cur = self.con.cursor()
        except sqlite3.OperationalError:
            print('ERROR | Ошибка загрузки базы данных!\nВозможно она используется другой программой.')
            sys.exit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nickname TEXT, password TEXT, xp INTEGER DEFAULT (0), lvl DEFAULT (1), kills DEFAULT (0), 
                floor DEFAULT (0));""")

    def disconnect(self):
        self.con.close()

    def request(self, text, params=None, commit=False):
        request = self.cur.execute(f"""{text}""", params)
        if not commit:
            return request.fetchall()
        else:
            self.con.commit()
        return True

    def register(self, nickname, password):
        result = self.request("SELECT nickname FROM accounts WHERE nickname = ?", params=[nickname])
        if len(result) != 0:
            return 'Данный никнейм занят!'
        self.request("INSERT INTO accounts (nickname, password) VALUES (?, ?)", params=[nickname, password],
                            commit=True)
        self.nickname = nickname
        return True

    def login(self, nickname, password):
        result = self.request("SELECT nickname FROM accounts WHERE nickname = ? AND password = ?",
                              params=[nickname, password])
        if len(result) == 0:
            return 'Неверный логин или пароль!'
        else:
            self.nickname = nickname
        return True

    def save_result(self, xp, lvl, kills, floor):
        self.request("UPDATE accounts SET xp = ?, lvl = ?, kills = ?, floor = ? WHERE nickname = ?",
                     params=[xp, lvl, kills, floor, self.nickname], commit=True)
        return True

    def get_result(self):
        return self.request("SELECT * FROM accounts WHERE nickname = ?", params=[self.nickname])[0]

    def get_top(self, key="lvl"):
        return self.cur.execute(f"SELECT nickname, {key} FROM accounts ORDER BY accounts.{key} DESC").fetchall()
