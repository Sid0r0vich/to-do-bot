import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

class TaskRepository:
    def __init__(self, db_file):
        self.connection = create_connection(db_file)
        self.create_table()

    def create_table(self):
        try:
            sql_create_tasks_table = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_text TEXT NOT NULL,
                day INTEGER NOT NULL
            );
            """
            cursor = self.connection.cursor()
            cursor.execute(sql_create_tasks_table)
        except Error as e:
            print(e)

    def add_task(self, user_id, task_text, day):
        sql = '''INSERT INTO tasks(user_id, task_text, day) VALUES(?, ?, ?)'''
        cursor = self.connection.cursor()
        cursor.execute(sql, (user_id, task_text, day))
        self.connection.commit()

        return cursor.lastrowid

    def delete_task(self, user_id, task_text) -> bool:
        sql = '''DELETE FROM tasks WHERE user_id = ? AND task_text = ?'''
        cursor = self.connection.cursor()
        cursor.execute(sql, (user_id, task_text))
        self.connection.commit()

        return cursor.rowcount >= 1

    def get_task_by_id(self, task_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id=", (task_id,))

        return cursor.fetchone()

    def get_all_user_tasks(self, user_id, day) -> iter:
        cursor = self.connection.cursor()
        cursor.execute("SELECT task_text FROM tasks WHERE user_id=? AND day=?", (user_id, day))

        return map(lambda row: row[0], cursor.fetchall())

    def get_old_user_tasks(self, user_id, day) -> iter:
        cursor = self.connection.cursor()
        cursor.execute("SELECT task_text FROM tasks WHERE user_id=? AND day<?", (user_id, day))

        return map(lambda row: row[0], cursor.fetchall())


todolist = [
    "Сделать домашнее задание по виртуализации",
    "Погулять с собакой"
]
