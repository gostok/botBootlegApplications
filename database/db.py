import sqlite3

conn = sqlite3.connect('audio_files.db')
c = conn.cursor()

# Создание таблицы для хранения данных материалов
c.execute('''
CREATE TABLE IF NOT EXISTS audio_uploads (
    user_id INTEGER,
    audio_count INTEGER,
    audio_file_path TEXT
)
''')

conn.commit()
conn.close()

def update_audio_count(user_id):
    conn = sqlite3.connect('audio_files.db', timeout=5)
    c = conn.cursor()

    # Проверяем, существует ли пользователь
    c.execute('SELECT audio_count FROM audio_uploads WHERE user_id = ?', (user_id,))
    result = c.fetchone()

    if result:
        audio_count = result[0] + 1
        c.execute('UPDATE audio_uploads SET audio_count = ? WHERE user_id = ?', (audio_count, user_id))
    else:
        audio_count = 1
        c.execute('INSERT INTO audio_uploads (user_id, audio_count) VALUES (?, ?)', (user_id, audio_count))

    conn.commit()
    conn.close()
    return audio_count

def get_user_count():
    conn = sqlite3.connect('audio_files.db', timeout=5)
    c = conn.cursor()

    c.execute('SELECT COUNT(DISTINCT user_id) FROM audio_uploads')
    res = c.fetchone()

    conn.close()
    return res[0] if res else 0

def get_audio_count():
    conn = sqlite3.connect('audio_files.db', timeout=5)
    c = conn.cursor()

    c.execute('SELECT SUM(audio_count) FROM audio_uploads')
    res = c.fetchone()

    conn.close()
    return res[0] if res and res[0] is not None else 0