from telethon.sync import TelegramClient

try:
    import sqlite3
except ImportError:
    sqlite3 = None


class DataBase:
    def __init__(self, client: TelegramClient):
        if sqlite3 is None:
            return
        self.filename = "musicgram.db"
        self._conn = None
        c = self._cursor()
        c.execute("""select name from sqlite_master where type='table' and name ='telegram'""")
        if not c.fetchone():
            self._create_table(c, """telegram (
                                    last_name text,
                                    profile_photos integer
                                    )
                                    """)

    def _cursor(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.filename, check_same_thread=False)
        return self._conn.cursor()

    @staticmethod
    def _create_table(c, definition):
        c.execute("create table {}".format(definition))

    def generate(self, data: tuple):
        c = self._cursor()
        c.execute("""delete from telegram""")
        c.execute("""insert or replace into telegram values (?, ?)""", data)
        _all = c.execute("""select * from telegram""").fetchone()
        c.close()
        return _all

    def save(self):
        if self._conn is not None:
            self._conn.commit()
