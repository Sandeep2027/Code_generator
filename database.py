import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('code_assistant.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS codes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  description TEXT,
                  language TEXT,
                  code TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  code_id INTEGER,
                  rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                  comment TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (code_id) REFERENCES codes(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS versions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  code_id INTEGER,
                  version_code TEXT,
                  version_note TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (code_id) REFERENCES codes(id))''')
    
    conn.commit()
    conn.close()

def save_code(description, language, code):
    conn = sqlite3.connect('code_assistant.db')
    c = conn.cursor()
    c.execute('INSERT INTO codes (description, language, code) VALUES (?, ?, ?)',
              (description, language, code))
    code_id = c.lastrowid
    conn.commit()
    conn.close()
    return code_id

def save_feedback(code_id, rating, comment):
    conn = sqlite3.connect('code_assistant.db')
    c = conn.cursor()
    c.execute('INSERT INTO feedback (code_id, rating, comment) VALUES (?, ?, ?)',
              (code_id, rating, comment))
    conn.commit()
    conn.close()

def save_version(code_id, code, note):
    conn = sqlite3.connect('code_assistant.db')
    c = conn.cursor()
    c.execute('INSERT INTO versions (code_id, version_code, version_note) VALUES (?, ?, ?)',
              (code_id, code, note))
    conn.commit()
    conn.close()

def get_code_stats():
    conn = sqlite3.connect('code_assistant.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM codes')
    total_codes = c.fetchone()[0]
    c.execute('SELECT AVG(rating) FROM feedback')
    avg_rating = c.fetchone()[0] or 0
    conn.close()
    return {'total_codes': total_codes, 'avg_rating': round(avg_rating, 2)}