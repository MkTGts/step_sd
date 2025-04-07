from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, Group
import functools


engine = create_engine("sqlite:///data/db/app.db", echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)



class ServiceDB:
    '''Класс с методами для работы с базой данных, достпными дял всех пользователей.'''

    @staticmethod
    # декоратор для начала, закртыия сессии и принятия изменений в ней
    def with_session(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with Session() as session:
                data: list = func(*args, **kwargs)

                session.add_all(data)
                session.commit()
        return wrapper
    

    @with_session
    def create_ticket(self, 
                      user_id: int,  # id пользователя который создает заявку
                      group_id: int,  #  id группы в которой пользователь состоит
                      operator_id: int,  # id оператора группы
                      message: str,  # текст заявки, подается пользователем
                      created_at: str,  # дата созданяи заявки
                      closed_ar: str|None=None  # дата закрытия заявки. изначаль none
                      ):
        '''Метод создает новый тикет.'''
        pass


    @with_session
    def user_registration(self, 
                          invite_token: int,  # пользователь вводит токен для регистрации и по токену распределяется в свою группу
                          tg_id: int,  # tg id пользователя
                          username: str,  # юзернами пользователя в телеграме
                          fullname: str, group_id: int,  # имя введенное пользователем
                          user_ip: str="None",  # ip пользователя, вводится админом и оператором
                          user_geo: str="None"  # расположение рабочего места пользователя, вводится админом или оператором
                        ) -> list:
        '''Метод создания нового пользователя.'''
        new_user = User(
            tg_id = tg_id,
            username = username,
            fullname = fullname,
            group_id = group_id,
            user_ip = user_ip,
            user_geo = user_geo
        )
        return [new_user]
    


class UserServiceDB(ServiceDB):
    @ServiceDB.with_session
    def ticket_list(self,
                    user_id: str  # id пользователя для поиска по таблице тикетов
                    ) -> list:
        '''Метод возвращает список всех созданных пользователем тикетов в формате списка'''
        pass



class OperatorServiceDB(ServiceDB, UserServiceDB):
    @ServiceDB.with_session
    def edit_status(self):
        '''Метод изменения статуса тикета'''
        pass


    @ServiceDB.with_session
    def drop_ticket(self):
        '''Метод удаления тикета'''
        pass


    @ServiceDB.with_session
    def add_user_ip(self,
                    user_id: str  # id пользователя для таблицы users
                      ):
        '''Метод добавления ip адреса пользователю в таблице users'''
        pass


    @ServiceDB.with_session
    def add_user_geo(self,
                     user_id: str  # id пользователя для таблицы users
                     ):
        '''Метод добавлени  расположения рабочего места пользователя в таблице users'''
        pass
        


class AdminServiceDB(ServiceDB, UserServiceDB, OperatorServiceDB):
    @ServiceDB.with_session
    def create_group(self,
                         group_name: str,  # название группы 
                         invite_token: int  # токен для приглашения пользователя в группу
                         ):
        '''Создание новое группы'''
        pass


    @ServiceDB.with_session
    def create_user(self, 
                          invite_token: int,  # пользователь вводит токен для регистрации и по токену распределяется в свою группу
                          tg_id: int,  # tg id пользователя
                          username: str,  # юзернами пользователя в телеграме
                          fullname: str, group_id: int,  # имя введенное пользователем
                          user_ip: str="None",  # ip пользователя, вводится админом и оператором
                          user_geo: str="None"  # расположение рабочего места пользователя, вводится админом или оператором
                        ) -> list:
        '''Метод создания нового пользователя.
        Добавлен на случай если админу потребуется создать пользователя самому руками'''
        new_user = User(
            tg_id = tg_id,
            username = username,
            fullname = fullname,
            group_id = group_id,
            user_ip = user_ip,
            user_geo = user_geo
        )
        return [new_user]


    @ServiceDB.with_session    
    def drop_user(self):
        '''Метод удаления пользователя'''
        pass


    @ServiceDB.with_session
    def drop_group(self):
        '''Метод удаления группы'''
        pass


    @ServiceDB.with_session
    def show_user_list(self):
        '''Метод выводит список всех пользователей'''
        pass


    @ServiceDB.with_session
    def show_group_list(self):
        '''Метод выводит список всех групп'''
        pass

    































"""
def create_new_user(Session):
    with Session() as session:
        new_user = User(tg_id = 1234,
        username = "mktgts",
        fullname = "Maksims",
        group_id = 1,
        user_ip = "192.168.1.52",
        user_geo = "4 этаж")

        session.add_all([new_user])
        session.commit()"""




#create_new_user(Session)


#with Session() as session:
#    add_new_user()


#session.add_all([new_user])
#session.commit()

#us = session.query(User).first()
#print(us)

#session.close()




