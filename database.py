import sqlite3
import datetime

DATABASE = 'project.db'


class Database:
    def __init__(self):
        self.db = sqlite3.connect(DATABASE)
        self.cursor = self.db.cursor()

    def commit(self):
        self.db.commit()


class Answers(Database):
    def __init__(self):
        super().__init__()

    def add_answer(self, task_id, user_id):
        answers = self.cursor.execute("select task_id from answers where user_id = ?", (user_id,)).fetchall()
        if task_id not in [i[0] for i in answers]:
            self.cursor.execute("insert into answers (task_id, user_id, date) values(?, ?, ?)",
                                (task_id, user_id, datetime.date.today()))
            self.commit()

    def get_answers(self, user_id):
        return self.cursor.execute("select * from answers where user_id = ?", (user_id,)).fetchall()


class Tasks(Database):
    def __init__(self):
        super().__init__()

    def get_tasks(self, topic_id):
        return self.cursor.execute(f"select * from tasks where topic_id = {topic_id}").fetchall()

    def set_task(self, task_counter):
        task = self.cursor.execute('select title from tasks where id = ?', (task_counter,)).fetchone()
        return task

    def set_skipped_task(self, skipped_tasks):
        for i in range(len(skipped_tasks)):
            task = self.cursor.execute('select title from tasks where id = ?', (i,)).fetchone()
            return task

    def answer(self, task_counter):
        return self.cursor.execute('select answer from tasks where id = ?', (task_counter,)).fetchone()

    def add_task(self, index, title, answer):
        self.cursor.execute('insert into tasks(topic_id, title, answer) values(?, ?, ?)', (index, title, answer))
        self.commit()

    def get_topic_id(self, id):
        return self.cursor.execute('select topic_id from tasks where id = ?', (id, )).fetchone()[0]

    def get_tasks_count(self):
        return len(self.cursor.execute("select id from tasks").fetchall())


class Topics(Database):
    def __init__(self):
        super().__init__()

    def get_all_topics(self):
        return self.cursor.execute('select id from topics')

    def get_topics_dict(self) -> dict:
        topics = self.cursor.execute('select * from topics').fetchall()
        temp = {}
        for i, *elem in topics:
            temp[i] = elem[0]
        return temp


class Users(Database):
    def __init__(self):
        super().__init__()

    def get_user(self, login):
        return self.cursor.execute('select * from users where login = ?', (login,)).fetchone()

    def get_logins(self):
        return [i[0] for i in self.cursor.execute('select login from users').fetchall()]

    def add_users(self, login, password):
        self.cursor.execute('insert into users(login, password) values(?, ?)', (login, password))
        self.commit()

    def check_user(self, login, password):
        check_pass = self.cursor.execute('select * from users where login = ?', (login,)).fetchone()
        if check_pass is not None:
            return str(check_pass[2]) == password
        else:
            return False

    def change_password(self, password, login):
        self.cursor.execute(f"update users set password = '{password}' where login = '{login}'")
        self.commit()


class Var_tasks(Database):
    def __init__(self):
        super().__init__()


class Variants(Database):
    def __init__(self):
        super().__init__()
