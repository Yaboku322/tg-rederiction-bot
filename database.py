import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages ( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, username TEXT,
        text TEXT, timestamp TEXT
        )
                            """)
        self.conn.commit()

    def save_message(self, user_id, username, text, timestamp):
        self.cursor.execute(
            "INSERT INTO messages (user_id, username, text, timestamp) VALUES (?,?,?,?)",
            (user_id, username, text, timestamp)
        )
        self.conn.commit()

    def get_messages(self):
        self.cursor.execute("SELECT * FROM messages")
        return self.cursor.fetchall()

    def get_last_messages(self, limit=10):
        self.cursor.execute(
            "SELECT * FROM messages ORDER BY id DESC LIMIT?", (limit,)
        )
        return self.cursor.fetchall()
    def close(self):
        self.conn.close()
