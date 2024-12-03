import sqlite3

class Database:
    def __init__(self, db_name="database/demo_bot.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()  # Создаем курсор здесь
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                audio_count INTEGER DEFAULT 0
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS demos (
                demo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                audio_file_path TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        self.connection.commit()

    def add_user(self, user_id):
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (user_id) VALUES (?)
        ''', (user_id,))
        self.connection.commit()

    def update_audio_count(self, user_id):
        self.cursor.execute('''
            UPDATE users SET audio_count = audio_count + 1 WHERE user_id = ?
        ''', (user_id,))
        self.connection.commit()

    def get_audio_count(self, user_id):
        self.cursor.execute('SELECT audio_count FROM users WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()  # Получаем результат
        return result[0] if result else 0  # Проверяем, есть ли результат

    def add_demo(self, user_id, audio_file_path):
        self.cursor.execute('''
            INSERT INTO demos (user_id, audio_file_path) VALUES (?, ?)
        ''', (user_id, audio_file_path))
        self.connection.commit()

    def get_user_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM users')
        return self.cursor.fetchone()[0]

    def close(self):
        self.connection.close()

    def get_total_audio_count(self):
        self.cursor.execute('SELECT SUM(audio_count) FROM users')
        result = self.cursor.fetchone()
        return result[0] if result else 0

