import sqlite3

CONN = sqlite3.connect('task_manager.db')
CURSOR = CONN.cursor()
