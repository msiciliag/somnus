'''scripts for database operations'''
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    '''create a database connection to a SQLite database'''
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_db():
    '''create the database and tables'''
    conn = sqlite3.connect('somnus.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT
                );''')
    c.execute('''CREATE TABLE IF NOT EXISTS sleep_record (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    duration INTEGER
                );''')
    c.execute('''CREATE TABLE IF NOT EXISTS time_table (
                    type TEXT PRIMARY KEY, -- Type of day: work, weekend, holiday
                    sleep_hour TEXT, -- Sleep time HH:MM
                    wake_up_hour TEXT, -- Wake up time HH:MM
                    duration INTEGER -- Sleep duration in minutes
                );''')
    c.execute('''CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY,
                    type TEXT NOT NULL, -- 'wake_up' or 'sleep'
                    time INTEGER NOT NULL, -- Time in minutes before (-) or after (+) wake-up/sleep time
                    days TEXT, -- List of days separated by commas (e.g., 'Monday,Wednesday,Friday')
                    message TEXT, -- Reminder message
                    sound TEXT, -- Name of the sound file for the alarm
                    active INTEGER DEFAULT 1 -- 1 if active, 0 if not
                ); ''')
    print("Database created")
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print("with tables: " + str(c.fetchall()))
    conn.commit()
    conn.close()


def is_db():
    '''check if the database exists'''
    try:
        conn = sqlite3.connect('somnus.db')
        #check if there are tables
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        if len(tables) == 0:
            return False
        conn.close()
        return True
    except Error:
        return False

def get_user():
    '''get the user name from the database'''
    if not is_db():
        return ""
    conn = sqlite3.connect('somnus.db')
    c = conn.cursor()
    c.execute("SELECT value FROM config WHERE key='user'")
    user = c.fetchone()
    conn.close()
    return user[0]

def set_user(name):
    '''set the user name in the database'''
    insert_config('user', name)

def insert_config(key, value):
    '''insert a configuration value in the database'''
    conn = sqlite3.connect('somnus.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    set_user('Alice')
    print(is_db())
    print(get_user())
