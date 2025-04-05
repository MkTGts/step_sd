import sqlite3
import logging
import os


# инициализация логгера
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="a",
    encoding="utf-8",
    format= '[%(asctime)s] #%(levelname)-8s %(filename)s:'
       '%(lineno)d - %(name)s - %(message)s'
)

class DBService:
    def create_db(self) -> None:
        '''Функция по созданию базы данных, если еще не существует.'''
        connection = sqlite3.connect('./data/db/database.db')  # утанавливаем и создает базу данных
        cursor = connection.cursor()  # устанавливаем курсор

        # создание таблиц
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (  
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tg_id INTEGER,
                    username TEXT,
                    fullname TEXT,
                    group_id INTEGER,
                    user_ip TEXT,
                    user_geo TEXT,
                    FOREIGN KEY (group_id) REFERENCES Groups(group_id)
        )''')  

        cursor.execute('''CREATE TABLE IF NOT EXISTS Groups (
                       group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       group_name TEXT,
                       invite_token INTEGER,
                       operator_id INTEGER,
                       FOREIGN KEY (operator_id) REFERENCES Users(user_id))
        ''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Tickets (
                       ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER,
                       group_id INTEGER,
                       operator_id INTEGER,
                       message TEXT,
                       status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'closed')),
                       priority TEXT NOT NULL DEFAULT 'low' CHECK (priority IN ('low', 'medium', 'high')),
                       created_at TIMESTAMP,
                       closed_at TIMESTAMP,
                       FOREIGN KEY (user_id) REFERENCES Users(user_id),
                       FOREIGN KEY (group_id) REFERENCES Groups(group_id),
                       FOREIGN KEY (operator_id) REFERENCES Users(user_id)
                       )''')
        connection.commit()  # выполнение изменения
        connection.close()  # закрываем соединение 


class UserDBService(DBService):
    pass


class OperatorDBService(DBService):
    pass


class AdminDBService(DBService):
    pass

