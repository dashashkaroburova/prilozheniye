import sys
from random import randint

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLineEdit
from database import *

import matplotlib.pyplot as plt
import datetime as dt


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project.ui', self)
        self.stackedWidget.setCurrentIndex(0)
        self.setWindowTitle("MySocialScienceExam")
        self.setFixedSize(1101, 831)

        styles = '''
        QMainWindow{
        background-color: #E6E6FA;}
        QComboBox{
        background-color: white;}
        QComboBox QAbstractItemView{
        selection-background-color: #BA55D3;}
        QLabel{
        font-family: Lucida Sans Unicode;
        font-size: 20px;}
        QLabel#task {
        font-size: 15px;}
        QLabel#label_3 {
        font-size: 15px;}
        QLabel#label_4 {
        font-size: 15px;}
        QLabel#wa_text {
        font-size: 15px;}
        QPushButton{
        background-color: rgb(216,191,216);
        border-radius: 4px;
        font-family: Lucida Sans Unicode;
        font-size: 25px;}
        QPushButton#to_reg_btn {
        font-size: 15px}
        QPushButton#make_var {
        font-size: 15px}
        QPushButton#change_pass {
        font-size: 15px}
        QPushButton#update_pass {
        font-size: 15px}
        QPushButton#add {
        font-size: 15px}
        QPushButton#add_task_btn {
        font-size: 15px}
        QPushButton#profile_btn {
        font-size: 15px}
        QPushButton#else_task {
        font-size: 15px}
        QPushButton#ans_btn {
        font-size: 15px}
        QPushButton#end_btn {
        font-size: 15px}
        QPushButton#back1 {
        font-size: 15px}
        QPushButton#back2 {
        font-size: 15px}
        QPushButton#back3 {
        font-size: 15px}
        QPushButton#back4 {
        font-size: 15px}
        QPushButton#back5 {
        font-size: 15px}
        QPushButton#back6 {
        font-size: 15px}
        QPushButton#forget_password {
        font-size: 18px}'''
        self.setStyleSheet(styles)

        self.users = Users()
        self.tasks = Tasks()
        self.answers = Answers()
        self.class_topics = Topics()

        self.ent_btn.clicked.connect(self.entering)
        self.reg_btn.clicked.connect(self.registration)
        self.profile_btn.clicked.connect(self.open_profile)

        self.back1.clicked.connect(self.back)
        self.back2.clicked.connect(self.back)

        self.back3.clicked.connect(self.back_to_topics)
        self.back4.clicked.connect(self.back_to_topics)
        self.back5.clicked.connect(self.back_to_topics)
        self.back6.clicked.connect(self.back_to_topics)
        self.back7.clicked.connect(self.back_to_profile)

        self.to_ent_btn.clicked.connect(self.to_enter)
        self.to_reg_btn.clicked.connect(self.to_register)
        self.ans_btn.clicked.connect(self.change_task)
        self.update_pass.clicked.connect(self.update_password)

        self.topics.currentIndexChanged.connect(self.change_topic)
        self.make_var.clicked.connect(self.change_variant)
        self.else_task.clicked.connect(self.skip_task)
        self.end_btn.clicked.connect(self.end_tasks)
        self.add_task_btn.clicked.connect(self.add_task)

        self.add.clicked.connect(self.adding)

        self.forget_password.clicked.connect(self.update_password_enter)
        self.change_pass.clicked.connect(self.update_password_profile)

        self.pass_ent.setEchoMode(QLineEdit.Password)

        self.user = None
        self.cur_task = None
        self.list_tasks = []
        self.topic_ind = 1
        self.points = 0
        self.task_count = 0
        self.change_ind = 0
        self.a = True
        self.skipped_tasks = []
        self.wrong_tasks = []
        self.right_tasks = []

    def entering(self):
        self.stackedWidget.setCurrentIndex(2)

    def registration(self):
        self.stackedWidget.setCurrentIndex(1)

    def back(self):
        self.stackedWidget.setCurrentIndex(0)

    def back_to_topics(self):
        self.stackedWidget.setCurrentIndex(3)
        self.topics.setCurrentIndex(0)

    def back_to_profile(self):
        self.stackedWidget.setCurrentIndex(7)

    def to_enter(self):
        login = self.login_ent.toPlainText().strip()
        password = self.pass_ent.text().strip()
        print(self.users.check_user(login, password))
        if self.users.check_user(login, password):
            self.user = self.users.get_user(login)
            self.stackedWidget.setCurrentIndex(3)
        else:
            self.message.setText('Неверный логин или пароль')

    def to_register(self):
        login = self.login_reg.text()
        password = self.pass_reg.text()
        try:
            if len(password) == 0:
                self.error.setText('Вы не ввели пароль')
            elif len(login) == 0:
                self.error.setText('Вы не ввели логин')
            else:
                self.users.add_users(login, password)
                self.user = self.users.get_user(login)
                self.stackedWidget.setCurrentIndex(3)
        except sqlite3.IntegrityError:
            self.error.setText('Такой логин уже существует')

    def clear_tasks(self):
        self.right_tasks.clear()
        self.wrong_tasks.clear()

    def change_topic(self):
        self.topic_ind = self.topics.currentIndex()
        if self.topic_ind:
            self.stackedWidget.setCurrentIndex(4)
            self.list_tasks = list(enumerate(self.tasks.get_tasks(self.topic_ind), 1))
            self.clear_tasks()
            self.task_count = len(self.list_tasks)
            self.a = True
            self.change_task()

    def change_task(self):
        self.stackedWidget.setCurrentIndex(4)
        if self.list_tasks:
            if self.a:
                self.answer.setText('')
                self.task_ind, self.cur_task = self.list_tasks.pop(0)
                self.task.setText(f'Задание №{self.task_ind}\n\n\n{self.cur_task[2]}')
                self.a = False
            elif len(self.answer.text()) == 0:
                self.comm.setText('Введите ответ')
            elif str(self.cur_task[3]) == self.answer.text():
                self.answers.add_answer(self.cur_task[0], self.user[0])
                self.right_tasks.append(self.cur_task)
                self.answer.setText('')
                self.task_ind, self.cur_task = self.list_tasks.pop(0)
                self.task.setText(f'Задание №{self.task_ind}\n\n\n{self.cur_task[2]}')
            else:
                self.wrong_tasks.append((self.task_ind, *(self.cur_task[1:]), self.answer.text()))
                self.answer.setText('')
                self.task_ind, self.cur_task = self.list_tasks.pop(0)
                self.task.setText(f'Задание №{self.task_ind}\n\n\n{self.cur_task[2]}')

    def skip_task(self):
        self.stackedWidget.setCurrentIndex(4)
        self.list_tasks.append((self.task_ind, self.cur_task))
        self.a = True
        self.change_task()

    def end_tasks(self):
        self.stackedWidget.setCurrentIndex(5)
        self.ya_num.setText(f'{len(self.right_tasks)}')
        self.all_a_num.setText(f'{self.task_count}')
        title = ['Номер задания', 'Ваш ответ', 'Правильный ответ']
        self.wa_texts.setColumnCount(len(title))
        self.wa_texts.setHorizontalHeaderLabels(title)
        self.wa_texts.setRowCount(0)
        for i, row in enumerate(self.wrong_tasks):
            self.wa_texts.setRowCount(
                self.wa_texts.rowCount() + 1)
            self.wa_texts.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.wa_texts.setItem(i, 1, QTableWidgetItem(row[4]))
            self.wa_texts.setItem(i, 2, QTableWidgetItem(str(row[3])))

        # self.wa_texts.resizeColumnsToContents()

    def add_task(self):
        self.stackedWidget.setCurrentIndex(6)

    def adding(self):
        index = self.topics_add.currentIndex()
        title = self.task_add.text()
        answer = self.answer_add.text()
        if index == 0:
            self.error1.setText('Вы не выбрали тему')
        elif len(title) == 0:
            self.error1.setText('Вы не ввели задание')
        elif len(answer) == 0:
            self.error1.setText('Вы не ввели ответ')
        else:
            self.tasks.add_task(index, title, answer)
            self.stackedWidget.setCurrentIndex(3)
            self.task_added_txt.setText('Задание добавлено')
            self.task_add.setText('')
            self.answer_add.setText('')
            self.topics_add.setCurrentIndex(0)

    def change_password(self):
        self.stackedWidget.setCurrentIndex(8)

    def open_profile(self):
        self.stackedWidget.setCurrentIndex(7)
        temp = self.answers.get_answers(self.user[0])
        print(self.tasks.get_tasks_count())
        self.num_tasks.setText(f'{len(temp)} из {self.tasks.get_tasks_count()}')
        self.stat_table.setColumnCount(3)
        self.stat_table.setHorizontalHeaderLabels(['Дата', 'Тема', 'Количество'])

        dates = {elem[3]: {} for elem in temp}
        topics = self.class_topics.get_topics_dict()

        for elem in temp:
            n = topics[self.tasks.get_topic_id(elem[2])]
            dates[elem[3]][n] = dates[elem[3]].get(n, 0) + 1
        print(dates)
        self.stat_table.setRowCount(sum([len(i) for i in dates.values()]))
        count = 0
        for i, item in enumerate(dates.items()):
            self.stat_table.setItem(count, 0, QTableWidgetItem(item[0]))
            for topic, amount in item[1].items():
                self.stat_table.setItem(count, 1, QTableWidgetItem(topic))
                self.stat_table.setItem(count, 2, QTableWidgetItem(str(amount)))
                count += 1

        try:
            date1, date2 = list(dates.keys())[-2:]
            self.progress.setText(
                f"Прогресс за последние дни: {sum(dates[date2].values()) - sum(dates[date1].values())}")
        except IndexError:
            print("Пупупу")

        create_plots(dates, self.tasks.get_tasks_count())
        self.diagram1.setPixmap(QPixmap("delta_dates.png"))
        self.diagram2.setPixmap(QPixmap("progress.png"))

    def update_password(self):
        index = self.change_ind
        login = self.login.text()
        password = self.new_pass.text()
        if len(password) == 0:
            self.error_3.setText('Вы не ввели пароль')
        elif login not in self.users.get_logins():
            self.error_3.setText('Такого логина не существует')
        else:
            self.users.change_password(password, login)
            self.stackedWidget.setCurrentIndex(index)
            self.message.setText('Ваш пароль изменен')

    def update_password_profile(self):
        self.stackedWidget.setCurrentIndex(8)
        self.change_ind = 7

    def update_password_enter(self):
        self.stackedWidget.setCurrentIndex(8)
        self.change_ind = 2

    def change_variant(self):
        self.clear_tasks()
        # a = self.tasks.get_tasks(1)
        tasks = []
        for i in self.class_topics.get_all_topics():
            temp = self.tasks.get_tasks(i[0])
            if temp:
                tasks.append(temp[randint(0, len(temp) - 1)])
        self.stackedWidget.setCurrentIndex(4)
        self.list_tasks = list(enumerate(tasks, 1))
        self.task_count = len(self.list_tasks)
        self.a = True
        self.change_task()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def create_plots(dates: dict, tasks_count):
    dates[dt.date.today().isoformat()] = {}
    temp = list(dates.keys())
    current_day = temp.pop(0)
    while current_day != temp[-1]:
        date = dt.date.fromisoformat(str(current_day))
        date += dt.timedelta(days=1)
        if (current_day := date.isoformat()) not in temp:
            dates[current_day] = {}

    dates = {key: value for key, value in sorted(dates.items(), key=lambda x: dt.date.fromisoformat(x[0]))}
    x = ["-".join(i.split("-")[1:]) for i in dates.keys()][:20]
    y = list([sum(i.values()) for i in dates.values()])[:20]

    fig, ax = plt.subplots()

    ax.bar(x, y)
    ax.set(xlabel="Даты (Месяц-День)", ylabel="Количество задач", title="Прогресс по дням")

    ax.set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    fig.savefig("delta_dates.png")

    fig, ax = plt.subplots()
    y = [sum(y[:i + 1]) / tasks_count * 100 for i in range(len(y))]
    ax.bar(x, y)
    ax.set(xlabel="Даты (Месяц-День)", ylabel="Процент от общего количества задач", title="Прогресс по курсу")
    ax.set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    fig.savefig("progress.png")


if __name__ == '__main__':
    # dates = {'2022-01-27': {'Тема 1': 3}, '2022-01-30': {'second': 1, 'seventh': 1}, '2022-01-31': {'second': 2}}
    # create_plots(dates, 50)
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
